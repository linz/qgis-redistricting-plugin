# -*- coding: utf-8 -*-
"""LINZ Redistricting Plugin - Core Utilities

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

from qgis.core import (QgsVectorLayer,
                       QgsRuleBasedLabeling,
                       QgsVectorLayerSimpleLabeling)


class CoreUtils:
    """
    Utilities for core plugin components
    """

    @staticmethod
    def enable_labels_for_layer(layer: QgsVectorLayer, enabled: bool = True):
        """
        Either enables or disables the labels for a layer. Works with standard labels and rule based labels
        :param layer: layer to edit
        :param enabled: whether labels should be enabled
        """
        labeling = layer.labeling()

        if isinstance(labeling, QgsRuleBasedLabeling):

            def enable_label_rules(rule: QgsRuleBasedLabeling.Rule):
                """
                Recursively enable rule based labeling
                """
                rule.setActive(enabled)
                for c in rule.children():
                    enable_label_rules(c)

            enable_label_rules(labeling.rootRule())
        elif isinstance(labeling, QgsVectorLayerSimpleLabeling):
            settings = labeling.settings()
            settings.drawLabels = False
            labeling.setSettings(settings)

        layer.triggerRepaint()
