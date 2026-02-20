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
from qgis.PyQt.QtWidgets import QDialog, QWidget, QShortcut, QMessageBox
from qgis.core import QgsApplication, QgsFeature, QgsFeatureRequest, QgsExpression, QgsMapLayerProxyModel, QgsVectorLayer, Qgis
from qgis.gui import QgsAttributeDialog, QgsDockWidget, QgsMapLayerComboBox, QgsAttributeForm

from NavTable.gui.NTSelectByFormDialog import NTSelectByFormDialog
from NavTable.gui.NTExpressionBuilder import NTExpressionBuilder
from NavTable.gui.NTFieldSelect import NTFieldSelect

pluginPath = os.path.split(os.path.dirname(__file__))[0]
WIDGET, BASE = uic.loadUiType(
    os.path.join(pluginPath, 'ui', 'main_panel.ui'))


class NTMainPanel(QgsDockWidget):

    def __init__(self, iface, vlayer, parent=None):
        super(NTMainPanel, self).__init__(parent)
        
        self.container = QWidget()
        self.ui = WIDGET()
        self.ui.setupUi(self.container)
        self.setWidget(self.container)
        
        for name, obj in self.ui.__dict__.items():
            setattr(self, name, obj)

        self.iface = iface
        self.layer = vlayer
        self.currentExpression = ''
        self.is_sorted = False

        self.layerCB = QgsMapLayerComboBox()
        self.layerCB.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.layerCB.setLayer(self.layer)
        self.layerCB.layerChanged.connect(self.change_layer)
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
        self.zoomBT.setIcon(QgsApplication.getThemeIcon('mActionZoomToSelected.svg'))
        self.panBT.setIcon(QgsApplication.getThemeIcon('mActionPanToSelected.svg'))
        self.deleteBT.setIcon(QgsApplication.getThemeIcon('mActionDeleteSelected.svg'))
        self.saveBT.setIcon(QgsApplication.getThemeIcon('mActionSaveEdits.svg'))
        self.editBT.setIcon(QgsApplication.getThemeIcon('mActionToggleEditing.svg'))

        self.previousDialog = self.widget_form
        self.validator = QIntValidator(1, 1)
        self.currentFeatLB.setValidator(self.validator)

        # Connect signals
        self.nextBT.clicked.connect(self.next)
        self.previousBT.clicked.connect(self.previous)
        self.lastBT.clicked.connect(self.last)
        self.firstBT.clicked.connect(self.first)
        self.orderByBT.clicked.connect(self.orderBy)
        self.exprFilterBT.clicked.connect(self.filter_by_expression)
        self.removeFilterBT.clicked.connect(self.removeFilter)
        self.deleteBT.clicked.connect(self.deleteFeature)
        self.currentFeatLB.returnPressed.connect(self.manual)
        self.zoomBT.clicked.connect(self.manual_zoom)
        self.panBT.clicked.connect(self.manual_pan)
        self.selectBT.clicked.connect(self.toggle_selection)
        self.saveBT.clicked.connect(self.save_edits)
        self.editBT.clicked.connect(self.toggle_editing)
        self.selectCB.stateChanged.connect(self.update_ui_states)
        self.onlySelectedCB.stateChanged.connect(self.handle_only_selected_changed)

        self.layer.selectionChanged.connect(self.update_select_button_state)
        self.layer.selectionChanged.connect(self.updateNFeatLB)
        self.layer.selectionChanged.connect(self.handle_selection_sync)
        self.layer.editingStarted.connect(self.handle_editing_started)
        self.layer.editingStopped.connect(self.handle_editing_stopped)

        # Initial state
        self.refresh_ids()
        self.update_select_button_state()
        self.updateNFeatLB() 
        
        self.deleteBT.setEnabled(not self.layer.readOnly())
        self.deleteBT.setStyleSheet("background-color: #ffcccc; border: 1px solid red;")
        
        # Sync edit button state without triggering signals if possible
        self.editBT.blockSignals(True)
        self.editBT.setChecked(self.layer.isEditable())
        self.editBT.blockSignals(False)

    def handle_editing_started(self):
        self.editBT.setChecked(True)
        self.updateDialog(self.getFeature(self.currentFid))

    def handle_editing_stopped(self):
        self.editBT.setChecked(False)
        self.updateDialog(self.getFeature(self.currentFid))

    def toggle_editing(self):
        if self.layer.isEditable():
            if self.can_proceed():
                self.layer.commitChanges()
        else:
            self.layer.startEditing()

    def save_edits(self):
        if self.layer.isEditable():
            form = self.currentDialog.attributeForm()
            form.save()
            self.layer.commitChanges()
            self.iface.messageBar().pushMessage("NavTable", self.tr("Changes saved successfully"), level=Qgis.Success)

    def handle_only_selected_changed(self):
        self.refresh_ids()
        self.update_ui_states()

    def handle_selection_sync(self):
        if self.onlySelectedCB.isChecked():
            self.refresh_ids()

    def refresh_ids(self):
        if self.onlySelectedCB.isChecked():
            self.allIds = self.layer.selectedFeatureIds()
        elif self.currentExpression != '':
            expr = QgsExpression(self.currentExpression)
            selection = self.layer.getFeatures(QgsFeatureRequest(expr))
            self.allIds = [s.id() for s in selection]
        else:
            self.allIds = self.layer.allFeatureIds()

        self.currentIndexFid = 0
        if self.allIds:
            self.currentFid = self.allIds[self.currentIndexFid]
            self.update(self.currentFid, self.currentIndexFid)
        else:
            self.updateNFeatLB()

    def update_ui_states(self):
        if self.currentFid in self.layer.selectedFeatureIds():
            self.currentFeatLB.setStyleSheet("background-color: #fdfd96; color: black;")
        else:
            self.currentFeatLB.setStyleSheet("")

        if self.currentExpression != '' or self.onlySelectedCB.isChecked():
            self.exprFilterBT.setStyleSheet("background-color: #fdfd96; border: 1px solid #cca300;")
        else:
            self.exprFilterBT.setStyleSheet("")

        if self.is_sorted:
            self.orderByBT.setStyleSheet("background-color: #b0e0e6; border: 1px solid #5f9ea0;")
        else:
            self.orderByBT.setStyleSheet("")

    def update_select_button_state(self):
        if self.currentFid in self.layer.selectedFeatureIds():
            self.selectBT.setIcon(QgsApplication.getThemeIcon('mActionDeselectAll.svg'))
            self.selectBT.setToolTip(self.tr('Remove current feature from selection'))
        else:
            self.selectBT.setIcon(QgsApplication.getThemeIcon('mActionSelectRectangle.svg'))
            self.selectBT.setToolTip(self.tr('Add current feature to selection'))
        self.update_ui_states()

    def toggle_selection(self):
        if self.currentFid in self.layer.selectedFeatureIds():
            self.layer.deselect(self.currentFid)
        else:
            self.layer.select(self.currentFid)

    def manual_zoom(self):
        self.iface.mapCanvas().zoomToFeatureIds(self.layer, [self.currentFid])

    def manual_pan(self):
        feat = self.getFeature(self.currentFid)
        if feat and feat.geometry():
            self.iface.mapCanvas().setCenter(feat.geometry().centroid().asPoint())
            self.iface.mapCanvas().refresh()

    def can_proceed(self):
        if self.layer.isEditable() and self.layer.isModified():
            reply = QMessageBox.question(self, self.tr('Unsaved Changes'),
                                       self.tr('There are unsaved changes. Do you want to save them before proceeding?'),
                                       QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Save)
            
            if reply == QMessageBox.Save:
                form = self.currentDialog.attributeForm()
                form.save()
                self.layer.commitChanges()
                return True
            elif reply == QMessageBox.Discard:
                self.layer.rollBack()
                return True
            else:
                return False
        return True

    def change_layer(self, layer):
        if not self.can_proceed(): 
            self.layerCB.setLayer(self.layer)
            return
        if layer and isinstance(layer, QgsVectorLayer):
            try:
                self.layer.editingStarted.disconnect(self.handle_editing_started)
                self.layer.editingStopped.disconnect(self.handle_editing_stopped)
                self.layer.selectionChanged.disconnect(self.update_select_button_state)
                self.layer.selectionChanged.disconnect(self.updateNFeatLB)
                self.layer.selectionChanged.disconnect(self.handle_selection_sync)
                
                self.nextBT.clicked.disconnect(self.next)
                self.previousBT.clicked.disconnect(self.previous)
                self.lastBT.clicked.disconnect(self.last)
                self.firstBT.clicked.disconnect(self.first)
                self.orderByBT.clicked.disconnect(self.orderBy)
                self.exprFilterBT.clicked.disconnect(self.filter_by_expression)
                self.removeFilterBT.clicked.disconnect(self.removeFilter)
                self.deleteBT.clicked.disconnect(self.deleteFeature)
                self.currentFeatLB.returnPressed.disconnect(self.manual)
                self.zoomBT.clicked.disconnect(self.manual_zoom)
                self.panBT.clicked.disconnect(self.manual_pan)
                self.selectBT.clicked.disconnect(self.toggle_selection)
                self.saveBT.clicked.disconnect(self.save_edits)
                self.editBT.clicked.disconnect(self.toggle_editing)
                self.selectCB.stateChanged.disconnect(self.update_ui_states)
                self.onlySelectedCB.stateChanged.disconnect(self.handle_only_selected_changed)
            except:
                pass

            self.currentExpression = ''
            self.is_sorted = False
            self.setup_layer(layer)
        
    def setCounters(self, current, max):
        self.currentFeatLB.setText(current)
        self.nFeatLB.setText(max)
        self.validator.setRange(1, int(max.split(' ')[0]))

    def next(self):
        if not self.can_proceed(): return
        newIndex = self.currentIndexFid + 1
        newFid = self.allIds[newIndex]
        self.update(newFid, newIndex)

    def previous(self):
        if not self.can_proceed(): return
        newIndex = self.currentIndexFid - 1
        newFid = self.allIds[newIndex]
        self.update(newFid, newIndex)

    def last(self):
        if not self.can_proceed(): return
        newIndex = len(self.allIds) - 1
        newFid = self.allIds[newIndex]
        self.update(newFid, newIndex)

    def first(self):
        if not self.can_proceed(): return
        newIndex = 0
        newFid = self.allIds[newIndex]
        self.update(newFid, newIndex)

    def manual(self):
        if not self.can_proceed(): return
        newIndex = int(self.currentFeatLB.text()) - 1
        newFid = self.allIds[newIndex]
        self.update(newFid, newIndex)

    def update(self, newFid, newIndex):
        feat = self.getFeature(newFid)
        if not feat: return
        self.currentIndexFid = newIndex
        self.currentFid = newFid
        self.updateNFeatLB()
        self.updateCanvas(feat)
        self.updateDialog(feat)
        self.update_select_button_state()
        self.checkButtons()

    def updateCanvas(self, feat):
        if self.has_to_select():
            self.layer.selectByIds([self.currentFid])
        if self.has_to_zoom():
            self.manual_zoom()
        elif self.has_to_pan():
            self.manual_pan()

    def has_to_pan(self):
        return self.panCB.isChecked()

    def has_to_zoom(self):
        return self.zoomCB.isChecked()

    def has_to_select(self):
        return self.selectCB.isChecked()

    def updateNFeatLB(self):
        total_count = self.layer.featureCount()
        filtered_count = len(self.allIds)
        selected_count = self.layer.selectedFeatureCount()
        
        if self.currentExpression != '' or self.onlySelectedCB.isChecked():
            max_label = "{} ({})".format(filtered_count, total_count)
        else:
            max_label = str(total_count)
            
        if selected_count > 0:
            max_label += " ({})".format(selected_count)
            self.removeFilterBT.setEnabled(True)
        elif self.currentExpression == '' and not self.is_sorted:
            self.removeFilterBT.setEnabled(False)
            
        self.setCounters(str(self.currentIndexFid + 1), max_label)
        self.update_ui_states()

    def getFeature(self, fid):
        feat = QgsFeature()
        if self.layer.getFeatures(QgsFeatureRequest().setFilterFid(fid)).nextFeature(feat):
            return feat
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
        reply = QMessageBox.question(self, self.tr('Delete Feature'),
                                   self.tr('Are you sure you want to delete the current feature?'),
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply != QMessageBox.Yes: return

        self.layer.startEditing()
        if self.layer.deleteFeature(self.currentFid):
            self.layer.commitChanges()
            if self.currentFid in self.allIds: self.allIds.remove(self.currentFid)
            if not self.allIds: return
            if self.currentIndexFid >= len(self.allIds): self.currentIndexFid = len(self.allIds) - 1
            self.update(self.allIds[self.currentIndexFid], self.currentIndexFid)
        else:
            self.layer.rollBack()
            self.iface.messageBar().pushMessage("NavTable", self.tr("Error deleting feature"), level=Qgis.Critical)

    def filter_by_expression(self):
        dialog = NTExpressionBuilder(self.layer, self.currentExpression, self.iface)
        if dialog.exec_():
            self.filter(dialog.expressionBuilder.expressionText())

    def filter_by_form(self):
        dialog = NTSelectByFormDialog(self.layer, self.iface)
        if dialog.exec_():
            self.filter(dialog.expression)

    def removeFilter(self):
        self.filter('')
        self.is_sorted = False
        self.layer.removeSelection()
        self.removeFilterBT.setEnabled(False)
        self.update_ui_states()

    def filter(self, expression):
        self.currentExpression = expression
        self.is_sorted = False
        if self.currentExpression != '':
            self.removeFilterBT.setEnabled(True)
            self.setWindowTitle('NavTable - {} ({})'.format(self.layer.name(), self.tr('Filtered')))
        else:
            self.setWindowTitle('NavTable - ' + self.layer.name())
        self.refresh_ids()

    def orderBy(self):
        dialog = NTFieldSelect(self.layer)
        if dialog.exec_():
            featureRequest = dialog.generateFeatureRequest()
            featureRequest.setFilterFids(self.allIds)
            feats = self.layer.getFeatures(featureRequest)
            self.allIds = [f.id() for f in feats]
            self.is_sorted = True
            self.removeFilterBT.setEnabled(True)
            self.currentIndexFid = 0
            if self.allIds: self.update(self.allIds[self.currentIndexFid], self.currentIndexFid)
