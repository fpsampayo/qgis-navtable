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

from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QWidget, QDialogButtonBox
from qgis.PyQt.QtCore import Qt
from qgis.gui import QgsAttributeForm, QgsAttributeEditorContext

pluginPath = os.path.split(os.path.dirname(__file__))[0]


class NTSelectByFormDialog(QDialog):

    def __init__(self, layer, iface):
        super().__init__(None)
        self.setWindowModality(Qt.WindowModal)

        layout = QVBoxLayout()
        layout.setMargin(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        dlgContext = QgsAttributeEditorContext()
        dlgContext.setFormMode(QgsAttributeEditorContext.StandaloneDialog)
        dlgContext.setAllowCustomUi(False)

        self.form = QgsAttributeForm(layer, context=dlgContext, parent=self)
        self.form.setMode(3)
        self.configureForm()
        layout.addWidget(self.form)

        self.form.zoomToFeatures.connect(self.zoomToFeatures)

        self.form.closed.connect(self.close)

        self.setWindowTitle(self.tr('Filter NavTable Features by Form'))

        self.expression = ''

    def configureForm(self):
        '''
        Hack to modify QgsAttributeForm
        '''

        self.form.findChild(QWidget, 'searchButtonBox').hide()

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.buttonBox.accepted.connect(self.form.searchZoomTo)
        self.buttonBox.rejected.connect(self.reject)

        self.form.layout().addWidget(self.buttonBox)

    def zoomToFeatures(self, filter):

        self.expression = filter
        super().accept()
