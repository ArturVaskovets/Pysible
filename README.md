# Pysible for LAMP

Production version adapted for [LAMP](https://es.wikipedia.org/wiki/LAMP). Check it on https://pysible.asir4all.tk (if still available).


## Setup
Install LAMP and other requirements: 
```
apt install \
apache2 mysql-server \
libapache2-mod-wsgi-py3 \
python-virtualenv git
```

Create MySQL database and user:
```
CREATE DATABASE Pysible;
CREATE USER '<username>'@'localhost' IDENTIFIED BY '<password>';
GRANT ALL ON Pysible.* To '<username>'@'localhost';
```

Install the app:
- Go into web root folder: ```cd /var/www/html/```
- Clone the LAMP branch of the repo: ```git clone https://github.com/ArturVaskovets/Pysible.git -b LAMP```
- Change the owner of the folder to default Apache user: ```chown -R www-data:www-data Pysible/```
- Go into Pysible folder: ```cd Pysible/```
- Make a virtual environment in ```venv``` dir: ```virtualenv -p /usr/bin/python3.8 venv```
- Activate the venv: ```source venv/bin/activate```
- Install requirements: ```pip install -r requirements.txt```
- Edit ```config.py```. Change ```SECRET_KEY```, ```PROJECTS_DIR``` and !```SQLALCHEMY_DATABASE_URI```! variables if needed.
- Edit ```app.wsgi```. Change web root and venv path if needed.
- Export FLASK_APP variable: ```export FLASK_APP="$(pwd)/app.py"```
- Initialize the app (use ```-d``` option to add test users): ```flask init_app```
- Set up admin user (if registered): ```flask set_admin <username>```


## Configure Apache2
Edit the virtual host configuration - ```/etc/apache2/sites-available/000-default.conf```:
```
<VirtualHost *:80>
	ServerName pysible.com

	DocumentRoot /var/www/html/Pysible

	WSGIDaemonProcess pysible user=www-data group=www-data threads=5
	WSGIScriptAlias / /var/www/html/Pysible/app.wsgi

	<Directory /var/www/html/Pysible>
		WSGIProcessGroup pysible
		WSGIApplicationGroup %{GLOBAL}
		Require all granted
	</Directory>

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```
For HTTPS configuration enable ```mod_ssl``` and use this configuration:
```
<VirtualHost *:80>
	ServerName pysible.asir4all.tk
	Redirect / https://pysible.asir4all.tk:443
</VirtualHost>

<IfModule mod_ssl.c>
	<VirtualHost _default_:443>
		ServerName pysible.asir4all.tk
		DocumentRoot /var/www/html/Pysible

		WSGIDaemonProcess pysible user=www-data group=www-data threads=5
		WSGIScriptAlias / /var/www/html/Pysible/app.wsgi

		<Directory /var/www/html/Pysible>
			WSGIProcessGroup pysible
			WSGIApplicationGroup %{GLOBAL}
			Require all granted
		</Directory>

		ErrorLog ${APACHE_LOG_DIR}/error.log
		CustomLog ${APACHE_LOG_DIR}/access.log combined

		SSLEngine on

		SSLCertificateFile		/etc/letsencrypt/live/pysible.asir4all.tk/fullchain.pem
		SSLCertificateKeyFile	/etc/letsencrypt/live/pysible.asir4all.tk/privkey.pem
	</VirtualHost>
</IfModule>
```
Finally restart Apache2:
```
systemctl restart apache2
```


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