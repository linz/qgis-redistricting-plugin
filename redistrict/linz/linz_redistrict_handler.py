# -*- coding: utf-8 -*-
"""LINZ Redistricting Plugin - LINZ Specific Redistrict Handler

.. note:: This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""

__author__ = '(C) 2018 by Nyall Dawson'
__date__ = '20/04/2018'
__copyright__ = 'Copyright 2018, The QGIS Project'
# This will get replaced with a git SHA1 when you do a git archive
__revision__ = '$Format:%H$'

from redistrict.core.redistrict_handler import RedistrictHandler


class LinzRedistrictHandler(RedistrictHandler):
    """
    LINZ specific class for redistrict handling operations. Pushes
    redistricting operations into the target layer's
    edit buffer, and stages changes for dissolving electorate
    layer boundaries
    """

    def __init__(self, meshblock_layer, target_field, electorate_layer):
        """
        Constructor
        :param meshblock_layer: meshblock layer
        :param target_field: target field for districts
        :param electorate_layer: electoral district layer
        """
        super().__init__(target_layer=meshblock_layer, target_field=target_field)
        self.electorate_layer = electorate_layer
        self.pending_changes = []

    def end_edit_group(self):
        super().end_edit_group()
        self.pending_changes = []

    def discard_edit_group(self):
        super().discard_edit_group()
        self.pending_changes = []

    def assign_district(self, target_ids, new_district):
        """
        Queue up changes
        :param target_ids:
        :param new_district:
        :return:
        """
        if not super().assign_district(target_ids, new_district):
            return False

        self.pending_changes.append({'TARGET': target_ids, 'DISTRICT': new_district})
        return True
