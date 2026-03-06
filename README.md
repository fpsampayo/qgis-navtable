# NavTable

This project was started by [Francisco Puga](https://github.com/fpuga)
Continued by [Francisco P. Sampayo](https://github.com/fpsampayo)
And finally completed by [Pablo Sanxiao](https://github.com/psanxiao)

http://navtable.github.io/

Features:

* Visualization of vectorial layers data in records one by one.
* Use of qgis layer form configuration, including custom forms or controls
* Select, pan or zoom to active record
* Edit and delete records when layer is in editing mode
* Access to layers actions
* Filter by expression using Qgis Expression Builder
* Filter by form using QgsAttributeForm in search mode
* Sort features

## Try in a dockerized qgis. 
Inside the docker folder you can run `docker compsoe up -d` to start navTable in qgis 3.44.
You can change the qgis version editing the `docker-compose.yml` file, line 3, to a existing version on  https://hub.docker.com/r/qgis/qgis/tags

