
PLUGINNAME = NavTable

VERSION=$(shell cat src/NavTable/metadata.txt | awk -F '=' '/^version/{print $$NF}')

package:
	rm -f build/$(PLUGINNAME)*.zip
	mkdir -p build
	cd src && cp -r $(PLUGINNAME) ../build/
	cp LICENSE README.md build/$(PLUGINNAME)/
	cd build && zip -9r $(PLUGINNAME)-$(VERSION).zip $(PLUGINNAME) && rm -rf $(PLUGINNAME)
	echo "Created package: $(PLUGINNAME)-$(VERSION).zip"