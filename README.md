##Instrunctions, Git CLone the repo


cd in "repo"
run $ docker build -t "sav/hgt_geoserver" .

docker run --name "geoserver" -d -p 8080:8080 sav/hgt_geoserver 

List available running containers

docker ps -a 

Clone the Repo and Rebuild. 

Credits to """"""


