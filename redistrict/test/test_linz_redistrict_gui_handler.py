# coding=utf-8
"""LINZ Redistrict GUI Handler Test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = '(C) 2018 by Nyall Dawson'
__date__ = '1/05/2018'
__copyright__ = 'Copyright 2018, The QGIS Project'
# This will get replaced with a git SHA1 when you do a git archive
__revision__ = '$Format:%H$'

import unittest
from qgis.core import (QgsVectorLayer,
                       QgsFeature)

from redistrict.linz.linz_district_registry import LinzElectoralDistrictRegistry
from redistrict.linz.linz_redistrict_gui_handler import LinzRedistrictGuiHandler
from redistrict.gui.redistricting_dock_widget import RedistrictingDockWidget
from .utilities import get_qgis_app

QGIS_APP, CANVAS, IFACE, PARENT = get_qgis_app()


class LinzRedistrictingGuiHandlerTest(unittest.TestCase):
    """Test LINZ RedistrictGuiHandler."""

    def testShowStats(self):
        """Test show stats for district"""
        layer = QgsVectorLayer(
            "Point?crs=EPSG:4326&field=fld1:string&field=fld2:string&field=type:string",
            "source", "memory")
        f = QgsFeature()
        f.setAttributes(["test4", "xtest1", 'GN'])
        f2 = QgsFeature()
        f2.setAttributes(["test2", "xtest3", 'GS'])
        f3 = QgsFeature()
        f3.setAttributes(["test3", "xtest3", 'M'])
        layer.dataProvider().addFeatures([f, f2, f3])
        registry = LinzElectoralDistrictRegistry(
            source_layer=layer,
            source_field='fld1',
            title_field='fld2')

        dock = RedistrictingDockWidget(IFACE)
        handler = LinzRedistrictGuiHandler(redistrict_dock=dock, district_registry=registry)

        handler.show_stats_for_district('')
        self.assertFalse(dock.frame.toPlainText())
        handler.show_stats_for_district('test4')
        self.assertIn('Statistics for xtest1', dock.frame.toPlainText())
        self.assertIn('General North Island', dock.frame.toPlainText())
        handler.show_stats_for_district('test3')
        self.assertIn('Statistics for xtest3', dock.frame.toPlainText())
        self.assertIn('Māori', dock.frame.toPlainText())


if __name__ == "__main__":
    suite = unittest.makeSuite(LinzRedistrictingGuiHandlerTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
