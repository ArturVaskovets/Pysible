# Pysible for Docker

Production version adapted for [Docker](https://www.docker.com/). Also available on [Docker Hub](https://hub.docker.com/r/arturvaskovets/pysible).


## Setup
Install Docker: 
```
apt update
apt install \
	apt-transport-https \
	ca-certificates \
	curl gnupg2 \
	software-properties-common
curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
add-apt-repository \
	"deb [arch=arm64] https://download.docker.com/linux/debian \
	$(lsb_release -cs) \
	stable"
apt update
apt install \
	docker-ce \
	docker-ce-cli \
	containerd.io
systemctl enable docker
```

## If you want to build it yourself:
- Clone the Docekr branch of the repo: ```git clone https://github.com/ArturVaskovets/Pysible.git -b Docker```
- Go into Pysible folder: ```cd Pysible/```
- Edit any file if needed.
- Build the image of Pysible: ```docker build -t pysible .```
- Run database container (MySQL): ```docker run --name mysql_server -e MYSQL_DATABASE=pysible -e MYSQL_ROOT_PASSWORD=<password> -d mysql```
- Wait 10 seconds. It's really important for initialize the app correctly.
- Run web app container: ```docker run --name pysible -e MYSQL_PASSWORD=<password> -p 80:80 --link mysql_server:mysql -d pysible```
- Open Bash in container: ```docker exec -i -t pysible /bin/bash```
- Set up admin user (if registered): ```flask set_admin <username>```


## If you only want to use it:
- Run database container (MySQL): ```docker run --name mysql_server -e MYSQL_DATABASE=pysible -e MYSQL_ROOT_PASSWORD=<password> -d mysql```
- Wait 10 seconds. It's really important for initialize the app correctly.
- Run web app container from Docker Hub: ```docker run --name pysible -e MYSQL_PASSWORD=<password> -p 80:80 --link mysql_server:mysql -d arturvaskovets/pysible```
- Open Bash in container: ```docker exec -i -t pysible /bin/bash```
- Set up admin user (if registered): ```flask set_admin <username>```


## CLI Commands
- ```flask --help``` - show command list/description.
- ```flask init_app [-d|--debug]``` - prepare the app to use. Debug mode adds some test users to the database.
- ```flask show_users``` - show all registered users.
- ```flask set_admin [-u|--unset] <username>``` - change the status of the user.
- ```flask db create [-w|--with_data]``` - create the model. ```-w``` adds some test users to the database.
- ```flask db drop``` - drop the model.
- ```flask db recreate``` - drop and create the model. May be userful if there are changes in the model.
- ```flask db add_data``` - import some test users from ```test_users.json``` to the database. 
- ```flask db import_templates``` - import Ansible templates from ```templates.json``` 
- ```flask db wipe_projects``` - delete all the projects both from database and from filesystem. It does not delete the model.