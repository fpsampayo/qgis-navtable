
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
import math

from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIntValidator, QKeySequence
from qgis.PyQt.QtWidgets import QDialog, QWidget, QShortcut
from qgis.core import QgsApplication, QgsFeature, QgsFeatureRequest, QgsExpression, QgsMapLayerProxyModel, QgsVectorLayer
from qgis.gui import QgsAttributeDialog, QgsDockWidget, QgsMapLayerComboBox

from NavTable.gui.NTSelectByFormDialog import NTSelectByFormDialog
from NavTable.gui.NTExpressionBuilder import NTExpressionBuilder
from NavTable.gui.NTFieldSelect import NTFieldSelect

pluginPath = os.path.split(os.path.dirname(__file__))[0]
WIDGET, BASE = uic.loadUiType(
    os.path.join(pluginPath, 'ui', 'main_panel.ui'))


class NTMainPanel(QgsDockWidget):

    def __init__(self, iface, vlayer, parent=None):
        super(NTMainPanel, self).__init__(parent)
        
        # Load UI into a container widget
        self.container = QWidget()
        self.ui = WIDGET()
        self.ui.setupUi(self.container)
        self.setWidget(self.container)
        
        # Inject UI elements into self for easier access
        for name, obj in self.ui.__dict__.items():
            setattr(self, name, obj)

        self.iface = iface
        self.layer = vlayer

        # Create layer selector manually
        self.layerCB = QgsMapLayerComboBox()
        self.layerCB.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.layerCB.setLayer(self.layer)
        self.layerCB.layerChanged.connect(self.change_layer)
        
        # Add it to the top of the layout
        self.verticalLayout_2.insertWidget(0, self.layerCB)

        self.iface.currentLayerChanged.connect(self.handle_active_layer_changed)

        self.setup_shortcuts()
        self.setup_layer(self.layer)

    def setup_shortcuts(self):
        QShortcut(QKeySequence(Qt.Key_Right), self, self.next)
        QShortcut(QKeySequence(Qt.Key_Left), self, self.previous)
        QShortcut(QKeySequence(Qt.Key_Home), self, self.first)
        QShortcut(QKeySequence(Qt.Key_End), self, self.last)
        QShortcut(QKeySequence("Ctrl+F"), self, self.filter_by_expression)
        
        delete_shortcut = QShortcut(QKeySequence(Qt.Key_Delete), self)
        delete_shortcut.activated.connect(self.handle_delete_shortcut)

    def handle_delete_shortcut(self):
        if self.layer.isEditable():
            self.deleteFeature()

    def handle_active_layer_changed(self, layer):
        if layer and isinstance(layer, QgsVectorLayer) and layer != self.layer:
            self.layerCB.setLayer(layer)

    def setup_layer(self, layer):
        self.layer = layer
        self.setWindowTitle('NavTable - ' + self.layer.name())
        self.exprFilterBT.setIcon(QgsApplication.getThemeIcon('mIconExpressionSelect.svg'))
        self.removeFilterBT.setIcon(QgsApplication.getThemeIcon('mActionDeselectAll.svg'))
        self.orderByBT.setIcon(QgsApplication.getThemeIcon('sort.svg'))

        self.previousDialog = self.widget_form

        self.validator = QIntValidator(1, 1)
        self.currentFeatLB.setValidator(self.validator)

        self.nextBT.clicked.connect(self.next)
        self.previousBT.clicked.connect(self.previous)
        self.lastBT.clicked.connect(self.last)
        self.firstBT.clicked.connect(self.first)
        self.orderByBT.clicked.connect(self.orderBy)
        self.exprFilterBT.clicked.connect(self.filter_by_expression)
        self.removeFilterBT.clicked.connect(self.removeFilter)
        self.deleteBT.clicked.connect(self.deleteFeature)
        self.currentFeatLB.returnPressed.connect(self.manual)

        self.layer.editingStarted.connect(self.activateEdit)
        self.layer.editingStopped.connect(self.deactivateEdit)

        self.allIds = self.layer.allFeatureIds()
        self.currentIndexFid = 0
        self.currentFid = self.allIds[self.currentIndexFid]
        self.currentExpression = ''
        self.update(self.currentFid, self.currentIndexFid)

        self.removeFilterBT.setEnabled(False)
        if self.layer.isEditable():
            self.activateEdit()

    def change_layer(self, layer):
        if layer and isinstance(layer, QgsVectorLayer):
            # Disconnect previous layer signals to avoid leaks
            try:
                self.layer.editingStarted.disconnect(self.activateEdit)
                self.layer.editingStopped.disconnect(self.deactivateEdit)
            except:
                pass

            # Disconnect button signals to avoid multiple connections
            self.nextBT.clicked.disconnect(self.next)
            self.previousBT.clicked.disconnect(self.previous)
            self.lastBT.clicked.disconnect(self.last)
            self.firstBT.clicked.disconnect(self.first)
            self.orderByBT.clicked.disconnect(self.orderBy)
            self.exprFilterBT.clicked.disconnect(self.filter_by_expression)
            self.removeFilterBT.clicked.disconnect(self.removeFilter)
            self.deleteBT.clicked.disconnect(self.deleteFeature)
            self.currentFeatLB.returnPressed.disconnect(self.manual)

            self.setup_layer(layer)
        
    def setCounters(self, current, max):
        
        self.currentFeatLB.setText(current)
        self.nFeatLB.setText(max)

        self.validator.setRange(1, int(max))

    def next(self):
        newIndex = self.currentIndexFid + 1
        newFid = self.allIds[newIndex]
        self.update(newFid, newIndex)

    def previous(self):
        newIndex = self.currentIndexFid - 1
        newFid = self.allIds[newIndex]
        self.update(newFid, newIndex)

    def last(self):
        newIndex = len(self.allIds) - 1
        newFid = self.allIds[newIndex]
        self.update(newFid, newIndex)

    def first(self):
        newIndex = 0
        newFid = self.allIds[newIndex]
        self.update(newFid, newIndex)

    def manual(self):
        newIndex = int(self.currentFeatLB.text()) - 1
        newFid = self.allIds[newIndex]
        self.update(newFid, newIndex)

    def update(self, newFid, newIndex):
        feat = self.getFeature(newFid)
        if not feat:
            print("Error accesing index.")
            return
        self.currentIndexFid = newIndex
        self.currentFid = newFid
        self.updateNFeatLB()
        self.updateCanvas(feat)
        self.updateDialog(feat)
        self.checkButtons()

    def updateCanvas(self, feat):
        if self.has_to_select():
            self.layer.selectByIds([self.currentFid])

        geom = feat.geometry()
        if self.has_to_zoom():
            self.zoomTo(geom.boundingBox())  # TODO: be careful with crs
        elif self.has_to_pan():
            self.panTo(geom.centroid())  # TODO: be careful with crs

    def zoomTo(self, newExtent):
        '''
        newExtend is bbox
        '''
        self.iface.mapCanvas().setExtent(newExtent)
        self.iface.mapCanvas().refresh()

    def panTo(self, newCenter):
        '''
        newCenter is QgsPoint geometry
        Taked from: http://svn.reprojected.com/qgisplugins/trunk/refmap/refmap.py
        '''
        newCenterPoint = newCenter.asPoint()
        currentExtent = self.iface.mapCanvas().extent()
        currentCenter = currentExtent.center()
        dx = math.fabs(newCenterPoint.x() - currentCenter.x())
        dy = math.fabs(newCenterPoint.y() - currentCenter.y())
        if (newCenterPoint.x() > currentCenter.x()):
            currentExtent.setXMinimum(currentExtent.xMinimum() + dx)
            currentExtent.setXMaximum(currentExtent.xMaximum() + dx)
        else:
            currentExtent.setXMinimum(currentExtent.xMinimum() - dx)
            currentExtent.setXMaximum(currentExtent.xMaximum() - dx)
        if (newCenterPoint.y() > currentCenter.y()):
            currentExtent.setYMaximum(currentExtent.yMaximum() + dy)
            currentExtent.setYMinimum(currentExtent.yMinimum() + dy)
        else:
            currentExtent.setYMaximum(currentExtent.yMaximum() - dy)
            currentExtent.setYMinimum(currentExtent.yMinimum() - dy)
        self.iface.mapCanvas().setExtent(currentExtent)
        self.iface.mapCanvas().refresh()

    def has_to_pan(self):
        return self.panCB.isChecked()

    def has_to_zoom(self):
        return self.zoomCB.isChecked()

    def has_to_select(self):
        return self.selectCB.isChecked()

    def updateNFeatLB(self):
        self.setCounters(str(self.currentIndexFid + 1), str(len(self.allIds)))

    def getFeature(self, fid):
        feat = QgsFeature()
        if self.layer.getFeatures(QgsFeatureRequest().setFilterFid(fid)).nextFeature(feat):
            return feat
        else:
            # return False
            return feat

    def checkButtons(self):

        if self.currentIndexFid == len(self.allIds) - 1:
            self.nextBT.setEnabled(False)
            self.lastBT.setEnabled(False)
        else:
            self.nextBT.setEnabled(True)
            self.lastBT.setEnabled(True)

        if self.currentIndexFid == 0:
            self.previousBT.setEnabled(False)
            self.firstBT.setEnabled(False)
        else:
            self.previousBT.setEnabled(True)
            self.firstBT.setEnabled(True)

    def updateDialog(self, feat):

        if isinstance(self.previousDialog, QgsAttributeDialog):
            self.previousDialog.accept()
        self.currentDialog = QgsAttributeDialog(self.layer, feat, False, showDialogButtons=False)
        self.currentDialog.setWindowFlag(Qt.Widget)

        self.scrollArea.setWidget(self.currentDialog)
        self.previousDialog = self.currentDialog

    def deleteFeature(self):

        self.layer.deleteFeature(self.currentFid)
        self.allIds.remove(self.currentFid)

        if self.currentIndexFid >= len(self.allIds) - 1:
            self.currentIndexFid = self.currentIndexFid - 1
        newFid = self.allIds[self.currentIndexFid]
        self.update(newFid, self.currentIndexFid)

    def activateEdit(self):

        self.deleteBT.setEnabled(True)
        self.deleteBT.setStyleSheet("background-color: red")

    def deactivateEdit(self):

        self.deleteBT.setEnabled(False)
        self.deleteBT.setStyleSheet("")

    def filter_by_expression(self):

        dialog = NTExpressionBuilder(self.layer, self.currentExpression, self.iface)

        if dialog.exec_():
            expression = dialog.expressionBuilder.expressionText()
            self.filter(expression)

    def filter_by_form(self):

        dialog = NTSelectByFormDialog(self.layer, self.iface)

        if dialog.exec_():
            expression = dialog.expression
            self.filter(expression)

    def removeFilter(self):

        self.filter('')
        self.removeFilterBT.setEnabled(False)

    def filter(self, expression):

        self.currentExpression = expression

        if self.currentExpression != '':
            expr = QgsExpression(self.currentExpression)
            selection = self.layer.getFeatures(QgsFeatureRequest(expr))
            self.allIds = [s.id() for s in selection]
            self.setWindowTitle('NavTable - {} ({})'.format(self.layer.name(), self.tr('Filtered')))
            self.removeFilterBT.setEnabled(True)

        if len(self.allIds) == 0 or self.currentExpression == '':
            self.allIds = self.layer.allFeatureIds()
            self.setWindowTitle('NavTable - ' + self.layer.name())

        self.currentIndexFid = 0
        newFid = self.allIds[self.currentIndexFid]
        self.update(newFid, self.currentIndexFid)

    def orderBy(self):

        dialog = NTFieldSelect(self.layer)

        if dialog.exec_():

            featureRequest = dialog.generateFeatureRequest()
            featureRequest.setFilterFids(self.allIds)

            feats = self.layer.getFeatures(featureRequest)
            self.allIds = [f.id() for f in feats]

            self.currentIndexFid = 0
            newFid = self.allIds[self.currentIndexFid]
            self.update(newFid, self.currentIndexFid)
