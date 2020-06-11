# Pysible for PythonAnywhere

Production version adapted for [PythonAnywhere](https://www.pythonanywhere.com). Check it on https://pysible.pythonanywhere.com (if still available).


## Setup
- Create MySQL database and user using web interface.
- Start a Bash console.
- Clone the PythonAnywhere branch of the repo: ```git clone https://github.com/ArturVaskovets/Pysible.git -b PythonAnywhere```
- Go into Pysible folder: ```cd Pysible/```
- Make a virtual environment in ```venv``` dir: ```virtualenv -p /usr/bin/python3.8 venv```
- Activate the venv: ```source venv/bin/activate```
- Install requirements: ```pip install -r requirements.txt```
- Edit ```config.py```. Change ```SECRET_KEY```, ```PROJECTS_DIR``` and !```SQLALCHEMY_DATABASE_URI```! variables if needed.
- Edit ```app.wsgi```. Change web root and venv path if needed.
- Export FLASK_APP variable: ```export FLASK_APP="$(pwd)/app.py"```
- Initialize the app (use ```-d``` option to add test users): ```flask init_app```
- Set up admin user (if registered): ```flask set_admin <username>```
- Go back to web interface.
- Create a new web app.
- Enter virtual environment path.
- Copy app.wsgi content to the WSGI configuration file proposed by PythonAnywhere.
- Force HTTPS if needed.
- Finally, reload the app.


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