#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QToolButton
from qgis.PyQt.QtCore import Qt, QCoreApplication
from qgis.gui import QgsAttributeForm, QgsAttributeEditorContext

pluginPath = os.path.split(os.path.dirname(__file__))[0]

class NTSelectByFormDialog(QDialog):

    def __init__(self, layer, iface):
        super(NTSelectByFormDialog, self).__init__(None)
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
        super(NTSelectByFormDialog, self).accept()
        
