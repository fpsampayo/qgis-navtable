#/***************************************************************************
# Navtable
# 
# Navtable
#                             -------------------
#        begin                : 2013-11-30
#        copyright            : (C) 2013 by fpuga
#        email                : fpuga@cartolab.es
# ***************************************************************************/
# 
#/***************************************************************************
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# ***************************************************************************/

# Makefile for a PyQGIS plugin 

# translation
FORMS = ../ui/main_panel.ui ../ui/field_select.ui ../ui/expressionBuilderDialog.ui
SOURCES = ../navtable.py ../gui/NTExpressionBuilder.py ../gui/NTFieldSelect.py ../gui/NTMainPanel.py ../gui/NTSelectByFormDialog.py
TRANSLATIONS = i18n/navtable_en.ts i18n/navtable_es.ts

# global

PLUGINNAME = NavTable

PY_FILES = __init__.py navtable.py

PY_MODULES = gui

EXTRAS = metadata.txt icon/icon.png

FOLDERS = icon ui

UI_FILES = ui/main_panel.ui ui/field_select.ui ui/expressionBuilderDialog.ui

HELP = help/build/html


%.qm : %.ts
	lrelease $<

deploy_temp: transclean transcompile
	rm -rf ./temp
	mkdir -p ./temp/$(PLUGINNAME)
	mkdir -p ./temp/$(PLUGINNAME)/$(PY_MODULES)
	cp -vrf $(PY_MODULES)/*.py ./temp/$(PLUGINNAME)/$(PY_MODULES)/
	cp -vf $(PY_FILES) ./temp/$(PLUGINNAME)/
	cp -vrf $(FOLDERS) ./temp/$(PLUGINNAME)/
	cp -vf metadata.txt ./temp/$(PLUGINNAME)/
	mkdir -p ./temp/$(PLUGINNAME)/i18n
	cp -vf i18n/*.qm ./temp/$(PLUGINNAME)/i18n/

zip: deploy_temp
	rm -f $(PLUGINNAME).zip
	cd ./temp; zip -9r $(CURDIR)/$(PLUGINNAME).zip $(PLUGINNAME)

# Create a zip package of the plugin named $(PLUGINNAME).zip. 
# This requires use of git (your plugin development directory must be a 
# git repository).
# To use, pass a valid commit or tag as follows:
#   make package VERSION=Version_0.3.2
package: compile
		rm -f $(PLUGINNAME).zip
		git archive --prefix=$(PLUGINNAME)/ -o $(PLUGINNAME).zip $(VERSION)
		echo "Created package: $(PLUGINNAME).zip"

# transup
# update .ts translation files
transup:
	pylupdate4 Makefile

# transcompile
# compile translation files into .qm binary format
transcompile: $(TRANSLATIONS:.ts=.qm)

# transclean
# deletes all .qm files
transclean:
	rm -f i18n/*.qm
