# coding=utf-8
"""LINZ Redistricting Handler test.

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

import unittest
from redistrict.linz.linz_redistrict_handler import (
    LinzRedistrictHandler
)
from qgis.core import (QgsVectorLayer,
                       QgsFeature,
                       NULL)


class LINZRedistrictHandlerTest(unittest.TestCase):
    """Test LinzRedistrictHandler."""

    def testBatched(self):
        """
        Test batched operations
        """
        meshblock_layer = QgsVectorLayer(
            "Polygon?crs=EPSG:4326&field=fld1:string&field=fld2:string",
            "source", "memory")
        f = QgsFeature()
        f.setAttributes(["test4", "xtest1"])
        f2 = QgsFeature()
        f2.setAttributes(["test2", "xtest3"])
        f3 = QgsFeature()
        f3.setAttributes(["test3", "xtest3"])
        f4 = QgsFeature()
        f4.setAttributes(["test1", NULL])
        f5 = QgsFeature()
        f5.setAttributes(["test2", "xtest2"])
        success, [f, f2, f3, f4, f5] = meshblock_layer.dataProvider().addFeatures([f, f2, f3, f4, f5])
        self.assertTrue(success)

        district_layer = QgsVectorLayer(
            "Polygon?crs=EPSG:4326&field=fld1:string&field=fld2:string",
            "source", "memory")

        handler = LinzRedistrictHandler(meshblock_layer=meshblock_layer, target_field='fld1',
                                        electorate_layer=district_layer)
        self.assertTrue(meshblock_layer.startEditing())
        handler.begin_edit_group('test')
        self.assertTrue(handler.assign_district([f.id(), f3.id()], 'aaa'))
        self.assertTrue(handler.assign_district([f5.id()], 'aaa'))

        # pending changes should be recorded
        self.assertEqual(handler.pending_changes,
                         [{'TARGET': [1, 3], 'DISTRICT': 'aaa'}, {'TARGET': [5], 'DISTRICT': 'aaa'}])
        handler.end_edit_group()
        self.assertFalse(handler.pending_changes)
        self.assertEqual([f['fld1'] for f in meshblock_layer.getFeatures()], ['aaa', 'test2', 'aaa', 'test1', 'aaa'])

        handler.begin_edit_group('test2')
        self.assertTrue(handler.assign_district([f2.id()], 'aaa'))
        self.assertTrue(handler.assign_district([f4.id()], 'aaa'))
        self.assertEqual(handler.pending_changes,
                         [{'DISTRICT': 'aaa', 'TARGET': [2]}, {'DISTRICT': 'aaa', 'TARGET': [4]}])
        handler.discard_edit_group()
        self.assertFalse(handler.pending_changes)
        self.assertEqual([f['fld1'] for f in meshblock_layer.getFeatures()], ['aaa', 'test2', 'aaa', 'test1', 'aaa'])


if __name__ == "__main__":
    suite = unittest.makeSuite(LINZRedistrictHandlerTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
