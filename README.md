# Pysible for SQLite

Development version adapted for [SQLite](https://www.sqlite.org/). Do not use in production.

## Setup
- Clone the SQLite branch of the repo: ```git clone https://github.com/ArturVaskovets/Pysible.git -b SQLite```
- Go into Pysible folder: ```cd Pysible/```
- Make a virtual environment in ```venv``` dir: ```virtualenv -p /usr/bin/python3.8 venv```
- Activate the venv: ```source venv/bin/activate```
- Install requirements: ```pip install -r requirements.txt```
- Modify ```config.py```. Change ```SECRET_KEY```, ```PROJECTS_DIR``` and ```SQLALCHEMY_DATABASE_URI``` variables if needed.
- Export FLASK_APP variable: ```export FLASK_APP="$(pwd)/app.py"```
- Initialize the app (use ```-d``` option to add test users): ```flask init_app```
- Set up admin user (if registered): ```flask set_admin <username>```
- Run the app: ```flask run -h 0.0.0.0 -p 80```

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