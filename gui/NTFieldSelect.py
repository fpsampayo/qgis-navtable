#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QCheckBox, QHBoxLayout
from qgis.PyQt.QtCore import Qt
from qgis.core import QgsFeatureRequest

pluginPath = os.path.split(os.path.dirname(__file__))[0]
WIDGET, BASE = uic.loadUiType(
    os.path.join(pluginPath, 'ui', 'field_select.ui'))

class NTFieldSelect(BASE, WIDGET):

    def __init__(self, layer):
        super(NTFieldSelect, self).__init__(None)
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowTitle(self.tr('Sort NavTable Features by field'))

        self.fieldSelectCB.setLayer(layer)
        self.fieldSelectCB2.setLayer(layer)
        self.fieldSelectCB3.setLayer(layer)

    def generateFeatureRequest(self):
        '''
        :return: A QgQgsFeatureRequests object with the orders defined in form
        '''

        featureRequest = QgsFeatureRequest()

        field1 = self.fieldSelectCB.currentField()
        ascending1 = self.sortOrderCB.isChecked()
        if field1 != '':
            featureRequest.addOrderBy(field1, ascending1)

        field2 = self.fieldSelectCB2.currentField()
        ascending2 = self.sortOrderCB2.isChecked()
        if field2 != '':
            featureRequest.addOrderBy(field2, ascending2, True)

        field3 = self.fieldSelectCB3.currentField()
        ascending3 = self.sortOrderCB3.isChecked()
        if field3 != '':
            featureRequest.addOrderBy(field3, ascending3, True)

        return featureRequest
