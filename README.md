# Pysible for Heroku

Production version adapted for [Heroku](https://www.heroku.com). Check it on https://pysible.herokuapp.com (if still available).


## Setup
This setup process does not support configuration files modification. If you need to modify something you need to fork this repository and push changes into. Then do the same steps with your repository.
- Create new app.
- Connect it to GitHub. Choose Heroku branch and deploy.
- Add Heroku Postgres add-on.
- Open console and run ```heroku run bash```
- Export FLASK_APP variable: ```export FLASK_APP="$(pwd)/app.py"```
- Initialize the app (use ```-d``` option to add test users): ```flask init_app```
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