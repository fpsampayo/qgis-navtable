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
# Import the PyQt and QGIS libraries
#from PyQt5.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt
#from PyQt5.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
#from .resources_rc import *
# Import the code for the dialog
from .navtabledialog import NavtableDialog
import os.path
import math


class Navtable:

    def __init__(self, iface):
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

        # Create the dialog (after translation) and keep reference
        self.dlg = NavtableDialog()
        # self.dlg.ui.panCB.clicked.connect(self.panClicked)
        # self.dlg.ui.zoomCB.clicked.connect(self.zoomClicked)
        # self.dlg.ui.selectCB.clicked.connect(self.foo)
        # self.dlg.ui.onlySelectedCB.clicked.connect(self.foo)
        self.dlg.ui.nextBT.clicked.connect(self.next)
        self.dlg.ui.previousBT.clicked.connect(self.previous)
        self.dlg.ui.lastBT.clicked.connect(self.last)
        self.dlg.ui.firstBT.clicked.connect(self.first)
        
    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/navtable/icon.png"),
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
        self.table = self.dlg.ui.attrsTable
        self.layer = self.iface.activeLayer()

        

        #Comprobamos si existe alguna capa y si esta es vectorial
        if self.layer == None or not isinstance(self.layer, QgsVectorLayer):
            QMessageBox.information(None, "Aviso", u"NavTable necesita una capa vectorial para funcionar.")
        else:
            # Lógica para poder ordenar los registros según un atributo
            # featureRequest = QgsFeatureRequest()
            # featureRequest.addOrderBy("parroquia", True)
            # feats = self.layer.getFeatures(featureRequest)
            # self.allIds = [f.id() for f in feats]
            # Lógica para poder ordenar los registros según un atributo

            self.allIds = self.layer.allFeatureIds()
            print(self.allIds)
            self.currentIndexFid = 0
            self.currentFid = self.allIds[self.currentIndexFid]
            feat = self.getFeature(self.currentFid)
            if not feat:
                print("Empty layer")

            self.dlg.ui.nFeatLB.setText(str(self.layer.featureCount()))
            self.dlg.setWindowTitle('NavTable - Capa: ' + self.layer.name())
            self.updateNFeatLB()
            self.printIt(feat)
            self.checkButtons()
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
        self.guardarDatos(self.currentFid)
        newIndex = self.currentIndexFid + 1
        newFid = self.allIds[newIndex]
        msg = "No more features - Disable next and last buttons"
        self.update(newFid, newIndex, msg)
        
    def previous(self):
        self.guardarDatos(self.currentFid)
        newIndex = self.currentIndexFid - 1
        newFid = self.allIds[newIndex]
        msg = "No more features - Disable previous and first buttons"
        self.update(newFid, newIndex, msg)

    def last(self):
        self.guardarDatos(self.currentFid)
        newIndex = len(self.allIds) - 1
        newFid = self.allIds[newIndex]
        msg = "Error. Should never happen"
        self.update(newFid, newIndex, msg)

    def first(self):
        self.guardarDatos(self.currentFid)
        newIndex = 0
        newFid = self.allIds[newIndex]
        msg = "Error. Error"
        self.update(newFid, newIndex, msg)        
    
    def update(self, newFid, newIndex, msg):
        feat = self.getFeature(newFid)
        if not feat:
            print(msg)
            return
        self.currentIndexFid = newIndex
        self.currentFid = newFid
        self.updateNFeatLB()
        self.updateCanvas(feat)
        self.printIt(feat)
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
        return self.dlg.ui.panCB.isChecked()

    def has_to_zoom(self):
        return self.dlg.ui.zoomCB.isChecked()
    
    def has_to_select(self):
        return self.dlg.ui.selectCB.isChecked()

    def updateNFeatLB(self):
        self.dlg.ui.currentFeatLB.setText(str(self.currentIndexFid + 1))

    def getFeature(self, fid):
        feat = QgsFeature()
        if self.layer.getFeatures( QgsFeatureRequest().setFilterFid( fid ) ).nextFeature( feat ):
            return feat
        else:
            #return False
            return feat


    def printIt(self, feat):
        #self.table.setText("")
        attrs = feat.attributes()

        #Insertamos el FID de la geometria
        # self.table.insertPlainText("FID - " + str(feat.id()))
        # self.table.insertPlainText("\n")

        self.table.setRowCount(len(attrs) + 2)
        
        numFilas = 0
        for n, v in enumerate(attrs):
            campo = QTableWidgetItem()
            valor = QTableWidgetItem()
            campo.setText(self.layer.attributeDisplayName(n))
            valor.setText(unicode(v))

            campo.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )

            self.table.setItem(numFilas, 0, campo)
            self.table.setItem(numFilas, 1, valor)

            numFilas = numFilas + 1

                
        geom = feat.geometry() 
        #Insertamos la longitud
        campo = QTableWidgetItem()
        valor = QTableWidgetItem()
        campo.setText("length")
        valor.setText(str(geom.length()))

        campo.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )

        self.table.setItem(numFilas, 0, campo)
        self.table.setItem(numFilas, 1, valor)
        #Comprobamos si es de tipo polygon
        if geom.type() == 2:
            campo = QTableWidgetItem()
            valor = QTableWidgetItem()
            campo.setText("area")
            valor.setText(str(geom.area()))   

            campo.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )

            self.table.setItem(numFilas + 1, 0, campo)
            self.table.setItem(numFilas + 1, 1, valor)



    def checkButtons(self):

        if self.currentIndexFid == len(self.allIds) - 1:
            self.dlg.ui.nextBT.setEnabled(False)
            self.dlg.ui.lastBT.setEnabled(False)
        else:
            self.dlg.ui.nextBT.setEnabled(True)
            self.dlg.ui.lastBT.setEnabled(True)

        if self.currentIndexFid == 0:
            self.dlg.ui.previousBT.setEnabled(False)
            self.dlg.ui.firstBT.setEnabled(False)
        else:
            self.dlg.ui.previousBT.setEnabled(True)
            self.dlg.ui.firstBT.setEnabled(True)

    '''
    This method generates a dict ready to update the feature attributes
    '''
    def guardarDatos(self, fid):

        if self.layer.isEditable():
            caps = self.layer.dataProvider().capabilities()

            newAttrs = {}
            for r in range(self.table.rowCount() - 2):
                for c in range(self.table.columnCount()):
                    newAttrs[r] = self.table.item(r, c).data(0)
            #print(newAttrs)

            if caps & QgsVectorDataProvider.ChangeAttributeValues:
                self.layer.dataProvider().changeAttributeValues({ fid : newAttrs })

