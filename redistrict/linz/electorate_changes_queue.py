# -*- coding: utf-8 -*-
"""LINZ Redistricting Plugin - Staged queue of electorate changes

.. note:: This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""

__author__ = '(C) 2018 by Nyall Dawson'
__date__ = '20/04/2018'
__copyright__ = 'Copyright 2018, LINZ'
# This will get replaced with a git SHA1 when you do a git archive
__revision__ = '$Format:%H$'

from typing import List
from qgis.core import (QgsVectorLayer,
                       QgsFeatureRequest,
                       QgsFeature)
from qgis.PyQt.QtWidgets import (QUndoCommand,
                                 QUndoStack)


class QueueItem(QUndoCommand):
    """
    Item within an ElectorateEditQueue
    """

    def __init__(self, electorate_layer: QgsVectorLayer,
                 previous_attributes: dict, previous_geometries: dict,
                 new_attributes: dict, new_geometries: dict,
                 user_log_layer: QgsVectorLayer,
                 user_log_entries: List[QgsFeature]):
        """
        Constructor
        :param electorate_layer: associated electorate layer
        :param previous_attributes: dictionary of previous attributes
        :param previous_geometries: dictionary of previous geometries
        :param new_attributes: dictionary of attribute edits
        :param new_geometries: dictionary of geometry edits
        :param user_log_layer: user log layer
        :param user_log_entries: user log entries associated with this change
        """
        super().__init__()
        self.electorate_layer = electorate_layer
        self.previous_attributes = previous_attributes
        self.previous_geometries = previous_geometries
        self.new_attributes = new_attributes
        self.new_geometries = new_geometries
        self.user_log_layer = user_log_layer
        self.user_log_entries = user_log_entries
        self.user_log_entry_fids = []

    def redo(self):  # pylint: disable=missing-docstring
        self.electorate_layer.dataProvider().changeGeometryValues(self.new_geometries)
        self.electorate_layer.dataProvider().changeAttributeValues(self.new_attributes)
        self.electorate_layer.triggerRepaint()

        self.user_log_entry_fids = [f.id() for f in
                                    self.user_log_layer.dataProvider().addFeatures(self.user_log_entries)[1]]

    def undo(self):  # pylint: disable=missing-docstring
        self.electorate_layer.dataProvider().changeGeometryValues(self.previous_geometries)
        self.electorate_layer.dataProvider().changeAttributeValues(self.previous_attributes)

        self.user_log_layer.dataProvider().deleteFeatures(self.user_log_entry_fids)
        self.user_log_entry_fids = []

        self.electorate_layer.triggerRepaint()

    def id(self):  # pylint: disable=missing-docstring
        return -1

    def mergeWith(self, other: 'QUndoCommand'):  # pylint: disable=missing-docstring, unused-argument
        return False


class ElectorateEditQueue(QUndoStack):
    """
    Queue for staged electorate edits, used when
    redistricting changes are created or rolled back
    to restore electorate layer to a matching state
    """

    def __init__(self, electorate_layer: QgsVectorLayer, user_log_layer: QgsVectorLayer):
        """
        Constructor
        :param electorate_layer: target electorate layer
        :param user_log_layer: user log layer
        """
        super().__init__()
        self.electorate_layer = electorate_layer
        self.user_log_layer = user_log_layer
        self.meshblock_undo_index = 0
        self.blocked = False

    def sync_to_meshblock_undostack_index(self, index: int):
        """
        Rollbacks the buffer (or rolls forward) to sync its state
        with the meshblock layer's undo buffer
        """
        if self.blocked:
            return

        is_back = index < self.meshblock_undo_index
        while self.meshblock_undo_index != index:
            if is_back:
                self.back()
                self.meshblock_undo_index -= 1
            else:
                self.forward()
                self.meshblock_undo_index += 1

    def rollback(self):
        """
        Rolls back the buffer to the start of the meshblock changes
        """
        self.sync_to_meshblock_undostack_index(0)

    def push_changes(self, attribute_edits: dict, geometry_edits: dict, log_entries: List[QgsFeature]):
        """
        Pushes a new set of electorate layer changes to the end of the queue
        :param attribute_edits: dictionary of attribute edits
        :param geometry_edits: dictionary of geometry edits
        :param log_entries: user log entries associated with this change
        """

        self.meshblock_undo_index += 1

        # record previous values
        attribute_feature_ids = list(attribute_edits.keys())
        request = QgsFeatureRequest().setFilterFids(attribute_feature_ids).setFlags(QgsFeatureRequest.NoGeometry)
        attributes = {f.id(): f.attributes() for f in self.electorate_layer.getFeatures(request)}
        prev_attributes = {
            feature_id: {attribute_index: attributes[feature_id][attribute_index] for attribute_index in v.keys()} for
            feature_id, v in attribute_edits.items()}

        geometry_feature_ids = list(geometry_edits.keys())
        request = QgsFeatureRequest().setFilterFids(geometry_feature_ids).setSubsetOfAttributes([])
        geometries = {f.id(): f.geometry() for f in self.electorate_layer.getFeatures(request)}
        prev_geometries = {feature_id: geometries[feature_id] for feature_id, v in geometry_edits.items()}

        self.push(QueueItem(self.electorate_layer, prev_attributes, prev_geometries, attribute_edits, geometry_edits,
                            self.user_log_layer,
                            log_entries))

    def back(self) -> bool:
        """
        Steps back one change in the queue
        :return: True if a step back was successful
        """
        if self.index() == 0:
            return False

        self.setIndex(self.index() - 1)
        return True

    def forward(self) -> bool:
        """
        Steps forward one change in the queue
        :return: True if a step forward was successful
        """
        if self.index() == self.count():
            return False

        self.setIndex(self.index() + 1)
        return True
