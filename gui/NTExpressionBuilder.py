#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt

pluginPath = os.path.split(os.path.dirname(__file__))[0]
WIDGET, BASE = uic.loadUiType(
    os.path.join(pluginPath, 'ui', 'expressionBuilderDialog.ui'))


class NTExpressionBuilder(BASE, WIDGET):

    def __init__(self, layer, expression):
        super(NTExpressionBuilder, self).__init__(None)
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.expressionBuilder = self.mExpressionBuilderWidget
        self.expressionBuilder.setLayer(layer)
        self.expressionBuilder.loadFieldNames()
        self.expressionBuilder.setExpressionText(expression)

    def accept(self):

        if self.expressionBuilder.isExpressionValid() or \
            self.expressionBuilder.expressionText() == '':
            super(NTExpressionBuilder, self).accept()
