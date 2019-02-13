#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt
from qgis.core import QgsApplication

pluginPath = os.path.split(os.path.dirname(__file__))[0]
WIDGET, BASE = uic.loadUiType(
    os.path.join(pluginPath, 'ui', 'base_panel.ui'))


class BasePanel(BASE, WIDGET):

    def __init__(self):
        super(BasePanel, self).__init__(None)
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.filterBT.setIcon(QgsApplication.getThemeIcon('/mIconExpressionSelect.svg'))