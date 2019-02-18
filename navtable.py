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
from qgis.PyQt.QtCore import QObject, QSettings, QTranslator, qVersion, QCoreApplication
from qgis.core import *
from qgis.core import QgsVectorLayer
from .gui.NTMainPanel import NTMainPanel
import os.path


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
            self.dlg = NTMainPanel(self.iface, self.layer)
            self.dlg.show()

            self.dlg.exec_()
