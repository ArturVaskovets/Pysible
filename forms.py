from flask_wtf import FlaskForm # pylint: disable=import-error
from wtforms import RadioField, BooleanField,StringField, SelectField, PasswordField, TextField # pylint: disable=import-error
from wtforms.fields.html5 import EmailField # pylint: disable=import-error
from wtforms.validators import Required # pylint: disable=import-error

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

