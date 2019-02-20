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
from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout
from qgis.PyQt.QtCore import Qt, QCoreApplication
from qgis.gui import QgsAttributeForm, QgsAttributeEditorContext

pluginPath = os.path.split(os.path.dirname(__file__))[0]


# noinspection PyPep8
class NTSelectByFormDialog(QDialog):

    def __init__(self, layer, iface):
        super().__init__(None)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

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
        :return:
        '''
        for c1 in self.form.children():
            for c2 in c1.children():
                for c3 in c2.children():
                    try:
                        if c3.text() == QCoreApplication.translate("QgsAttributeForm", "&Select features") or \
                                c3.text() == QCoreApplication.translate("QgsAttributeForm", "&Flash features"):
                            c3.hide()
                        elif c3.text() == QCoreApplication.translate("QgsAttributeForm", "&Zoom to features"):
                            c3.setText("Ok")
                    except:
                        pass

    def zoomToFeatures(self, filter):

        self.expression = filter
        super().accept()

