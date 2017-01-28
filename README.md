##Instrunctions, Git CLone the repo


cd in "repo"
run $ docker build -t "sav/hgt_geoserver" .

docker run --name "geoserver" -d -p 8080:8080 sav/hgt_geoserver 
docker run --name geoserver --restart=always -d -p 8080:8080 -v /data/geoserver_data:/opt/geoserver/data_dir sav/hgt_geoserver

List available running containers

docker ps -a 

Clone the Repo and Rebuild. 

Credits to """"""


