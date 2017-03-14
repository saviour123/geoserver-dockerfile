## Usage

This dockerfile helps you to deploy geoserver v10 on ubuntu. on docker containers. This is simple and straight 
forward.

#### Clone the Repository
`$ git clone https://github.com/saviour123/hgt_geoserver.git && cd hgt_geoserver`

#### Build the Docker Image
`$ docker build -t "sav/hgt_geoserver" .`

#### Run the image
`docker run --name "geoserver" -d -p 8080:8080 sav/hgt_geoserver` \\simple run.

#### Lets Run the Geoserver Persistent
`$ docker run --name geoserver --restart=always -d -p 8080:8080 -v /data/geoserver_data:/opt/geoserver/data_dir sav/hgt_geoserver`

### Miscellaneous
List available running containers:

`$ docker ps -a`


Clone the Repo and Rebuild. 

See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT)


