from flask_wtf import FlaskForm # pylint: disable=import-error
from wtforms import RadioField, BooleanField,StringField, SelectField, PasswordField, TextField # pylint: disable=import-error
from wtforms.fields.html5 import EmailField # pylint: disable=import-error
from wtforms.validators import Required, Length # pylint: disable=import-error

class MainForm(FlaskForm):
	#General
	playbook_name = StringField('Playbook name',default='playbook', validators=[Required('This field is required')])
	description = TextField('Description',default='')


	#Webservers section
	install_webserver = BooleanField('Install webserver', default=False)
	server_types = RadioField('Webserver type', choices=[('apache','Apache2'),('nginx','Nginx')], default='apache')
	document_root = StringField('Document root',default='/var/www/html')
	server_name = StringField('Server name',default='')


	#Interpreters section
	#PHP
	install_php = BooleanField('Install PHP', default=False)
	version_php = SelectField('Version', choices=[('', 'default'), ('7.0', '7.0'), ('7.1', '7.1'), ('7.2', '7.2'), ('7.3', '7.3')], default='')

	#Python
	install_python = BooleanField('Install Python', default=False)
	version_python = SelectField('Version', choices=[('', '2.7'), ('3', '3.5+')], default='')


	#Databases
	install_db = BooleanField('Install database', default=False)
	db_types = RadioField('Database type', choices=[('mysql','MySQL'),('postgresql','PostgreSQL'),('sqlite','SQLite')], default='mysql')
	db_delete_anonymous = BooleanField('Delete anonymous user', default=False)
	db_delete_test = BooleanField('Delete test database', default=False)
	db_create_user = BooleanField('Create user', default=False)
	db_username = StringField('Username', validators=[Length(message=u'Username length must be in the range 3-20 characters', min=3, max=20)], default='user')
	db_password = StringField('Password', validators=[Length(message=u'Password length must be in the range 6-20 characters', min=6, max=20)], default='password')


class LoginForm(FlaskForm):
	username = StringField('Username', validators=[Required('This field is required')])
	password = PasswordField('Password', validators=[Required('This field is required')])

class SignupForm(FlaskForm):
	username = StringField('Username', validators=[Required('This field is required')])
	password = PasswordField('Password', validators=[Required('This field is required')])
	name = StringField('Full name', validators=[Required('This field is required')])
	email = EmailField('Email')

class AccountEditForm(FlaskForm):
	username = StringField('Username', validators=[Required('This field is required')])
	password = PasswordField('New password', default='')
	name = StringField('Full name', validators=[Required('This field is required')])
	email = EmailField('Email')

