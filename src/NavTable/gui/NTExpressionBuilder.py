"""
/***************************************************************************
 Navtable
                                 A QGIS plugin
 Navtable
                              -------------------
        begin                : 2019-02-20
        copyright            : (C) 2013 by Francisco P. Sampayo
        email                : fpsampayo@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt

pluginPath = os.path.split(os.path.dirname(__file__))[0]
WIDGET, BASE = uic.loadUiType(
    os.path.join(pluginPath, 'ui', 'expressionBuilderDialog.ui'))


class NTExpressionBuilder(BASE, WIDGET):

    def __init__(self, layer, expression):
        super().__init__(None)
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.setWindowTitle(self.tr('Filter NavTable Features by Expression'))
        self.expressionBuilder = self.mExpressionBuilderWidget
        self.expressionBuilder.setLayer(layer)
        self.expressionBuilder.loadFieldNames()
        self.expressionBuilder.loadRecent()

        self.initialExpression = expression
        self.expressionBuilder.setExpressionText(expression)

    def accept(self):

        if self.initialExpression == self.expressionBuilder.expressionText():
            self.reject()
            return

        if self.expressionBuilder.isExpressionValid() or \
                self.expressionBuilder.expressionText() == '':
            self.expressionBuilder.saveToRecent()
            super().accept()
