# -*- coding: utf-8 -*-
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
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load Navtable class from file Navtable
    from .navtable import Navtable
    return Navtable(iface)
