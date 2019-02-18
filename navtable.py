# -*- coding: utf8 -*-

"""
/***************************************************************************
 Navtable
                                 A QGIS plugin
 Navtable
                              -------------------
        begin                : 2013-11-30
        copyright            : (C) 2013 by fpuga
        email                : fpuga@cartolab.es
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
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtCore import QObject, QSettings, QTranslator, qVersion, QCoreApplication, Qt
from qgis.core import *
from qgis.core import QgsFeature, QgsVectorLayer
from qgis.gui import QgsAttributeDialog
from .gui.basePanel import BasePanel
from .gui.NTExpressionBuilder import NTExpressionBuilder
from .gui.NTSelectByFormDialog import NTSelectByFormDialog
import os.path
import math


class Navtable(QObject):

    def __init__(self, iface):
        super(Navtable, self).__init__()
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'navtable_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
        
    def initGui(self):
        # Create action that will start plugin configuration
        icon_path = os.path.join(self.plugin_dir, 'icon', 'icon.png')
        self.action = QAction(
            QIcon(icon_path),
            u"Navtable", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&Navtable", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Navtable", self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):

        self.layer = self.iface.activeLayer()

        #Comprobamos si existe alguna capa y si esta es vectorial
        if self.layer == None or not isinstance(self.layer, QgsVectorLayer):
            self.iface.messageBar().pushMessage("Invalid Layer", "NavTable only works on a vector layer", level=Qgis.Warning)
        else:
            self.allIds = self.layer.allFeatureIds()
            #print(self.allIds)
            self.currentIndexFid = 0
            self.currentFid = self.allIds[self.currentIndexFid]
            self.currentExpression = ''
            feat = self.getFeature(self.currentFid)
            if not feat:
                print("Empty layer")

            # Create the dialog (after translation) and keep reference
            self.dlg = BasePanel()
            self.dlg.nextBT.clicked.connect(self.next)
            self.dlg.previousBT.clicked.connect(self.previous)
            self.dlg.lastBT.clicked.connect(self.last)
            self.dlg.firstBT.clicked.connect(self.first)
            self.dlg.exprFilterBT.clicked.connect(self.filter_by_expression)
            self.dlg.formFilterBT.clicked.connect(self.filter_by_form)

            self.dlg.deleteBT.clicked.connect(self.deleteFeature)
            self.dlg.currentFeatLB.returnPressed.connect(self.manual)

            self.layer.editingStarted.connect(self.activateEdit)
            self.layer.editingStopped.connect(self.deactivateEdit)

            self.previousDialog = self.dlg.widget_form

            self.dlg.nFeatLB.setText(str(self.layer.featureCount()))
            self.dlg.setWindowTitle('NavTable - ' + self.layer.name())
            self.updateNFeatLB()
            self.updateDialog(feat)
            self.checkButtons()
            if self.layer.isEditable():
                self.activateEdit()
            self.dlg.show()
            
            result = self.dlg.exec_()
            # See if OK was pressed
            if result == 1:
                pass



    def panClicked(self):
        print("pan: " + str(self.has_to_pan()))
        print("zoom: " + str(self.has_to_zoom()))
        
    def zoomClicked(self):
        print("pan: " + str(self.has_to_pan()))
        print("zoom: " + str(self.has_to_zoom()))

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
        newIndex = int(self.dlg.currentFeatLB.text()) - 1
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
            self.zoomTo(geom.boundingBox()) # TODO: be careful with crs
        elif self.has_to_pan():
            self.panTo(geom.centroid()) # TODO: be careful with crs


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
            currentExtent.setXMinimum( currentExtent.xMinimum() + dx )
            currentExtent.setXMaximum( currentExtent.xMaximum() + dx )
        else:
            currentExtent.setXMinimum( currentExtent.xMinimum() - dx )
            currentExtent.setXMaximum( currentExtent.xMaximum() - dx )
        if (newCenterPoint.y() > currentCenter.y()):
            currentExtent.setYMaximum( currentExtent.yMaximum() + dy )
            currentExtent.setYMinimum( currentExtent.yMinimum() + dy )
        else:
            currentExtent.setYMaximum( currentExtent.yMaximum() - dy )
            currentExtent.setYMinimum( currentExtent.yMinimum() - dy )
        self.iface.mapCanvas().setExtent(currentExtent)
        self.iface.mapCanvas().refresh()
            
    def has_to_pan(self):
        return self.dlg.panCB.isChecked()

    def has_to_zoom(self):
        return self.dlg.zoomCB.isChecked()
    
    def has_to_select(self):
        return self.dlg.selectCB.isChecked()

    def updateNFeatLB(self):
        self.dlg.setCounters(str(self.currentIndexFid + 1), str(len(self.allIds)))

    def getFeature(self, fid):
        feat = QgsFeature()
        if self.layer.getFeatures( QgsFeatureRequest().setFilterFid( fid ) ).nextFeature( feat ):
            return feat
        else:
            #return False
            return feat

    def checkButtons(self):

        if self.currentIndexFid == len(self.allIds) - 1:
            self.dlg.nextBT.setEnabled(False)
            self.dlg.lastBT.setEnabled(False)
        else:
            self.dlg.nextBT.setEnabled(True)
            self.dlg.lastBT.setEnabled(True)

        if self.currentIndexFid == 0:
            self.dlg.previousBT.setEnabled(False)
            self.dlg.firstBT.setEnabled(False)
        else:
            self.dlg.previousBT.setEnabled(True)
            self.dlg.firstBT.setEnabled(True)

    def updateDialog(self, feat):

        if isinstance(self.previousDialog, QgsAttributeDialog):
            self.previousDialog.accept()
        self.currentDialog = QgsAttributeDialog(self.layer, feat, False, showDialogButtons=False)
        self.currentDialog.setWindowFlag(Qt.Widget)

        self.dlg.scrollArea.setWidget(self.currentDialog)
        self.previousDialog = self.currentDialog

    def deleteFeature(self):

        self.layer.deleteFeature(self.currentFid)
        self.allIds.remove(self.currentFid)

        if self.currentIndexFid >= len(self.allIds) - 1:
            self.currentIndexFid = self.currentIndexFid - 1
        newFid = self.allIds[self.currentIndexFid]
        self.update(newFid, self.currentIndexFid)

    def activateEdit(self):

        self.dlg.deleteBT.setEnabled(True)
        self.dlg.deleteBT.setStyleSheet("background-color: red")

    def deactivateEdit(self):

        self.dlg.deleteBT.setEnabled(False)
        self.dlg.deleteBT.setStyleSheet("")

    def filter_by_expression(self):

        dialog = NTExpressionBuilder(self.layer, self.currentExpression)

        if dialog.exec_():
            expression = dialog.expressionBuilder.expressionText()
            self.filter(expression)

    def filter_by_form(self):

        dialog = NTSelectByFormDialog(self.layer, self.iface)

        if dialog.exec_():
            expression = dialog.expression
            self.filter(expression)

    def filter(self, expression):

        self.currentExpression = expression

        if self.currentExpression != '':
            expr = QgsExpression(self.currentExpression)
            selection = self.layer.getFeatures(QgsFeatureRequest(expr))
            self.allIds = [s.id() for s in selection]
            self.dlg.setWindowTitle('NavTable - {} ({})'.format(self.layer.name(), 'Filtered'))

        if len(self.allIds) == 0 or self.currentExpression == '':
            self.allIds = self.layer.allFeatureIds()
            self.dlg.setWindowTitle('NavTable - ' + self.layer.name())

        self.currentIndexFid = 0
        newFid = self.allIds[self.currentIndexFid]
        self.update(newFid, self.currentIndexFid)

    # Lógica para poder ordenar los registros según un atributo
    # featureRequest = QgsFeatureRequest()
    # featureRequest.addOrderBy("parroquia", True)
    # feats = self.layer.getFeatures(featureRequest)
    # self.allIds = [f.id() for f in feats]
    # Lógica para poder ordenar los registros según un atributo