#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIntValidator
from qgis.core import QgsApplication

pluginPath = os.path.split(os.path.dirname(__file__))[0]
WIDGET, BASE = uic.loadUiType(
    os.path.join(pluginPath, 'ui', 'base_panel.ui'))


class BasePanel(BASE, WIDGET):

    def __init__(self):
        super(BasePanel, self).__init__(None)
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.exprFilterBT.setIcon(QgsApplication.getThemeIcon('/mIconExpressionSelect.svg'))
        self.formFilterBT.setIcon(QgsApplication.getThemeIcon('/mIconFormSelect.svg'))

        self.validator = QIntValidator(1,1)
        self.currentFeatLB.setValidator(self.validator)
        
    def setCounters(self, current, max):
        
        self.currentFeatLB.setText(current)
        self.nFeatLB.setText(max)

        self.validator.setRange(1, int(max))

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Enter:
            pass
        else:
            super(BasePanel, self).keyPressEvent(event)