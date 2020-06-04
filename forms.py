from flask_wtf import FlaskForm # pylint: disable=import-error
from wtforms import RadioField, BooleanField,StringField, SelectField, PasswordField, TextField # pylint: disable=import-error
from wtforms.fields.html5 import EmailField # pylint: disable=import-error
from wtforms.validators import Required, Length, InputRequired, Optional # pylint: disable=import-error

class RequiredIf(InputRequired):
    """Validator which makes a field required if another field is set and has a truthy value."""
    field_flags = ('requiredif',)

    def __init__(self, other_field_name, message=None, *args, **kwargs):
        self.other_field_name = other_field_name
        self.message = message

    def __call__(self, form, field):
        other_field = form[self.other_field_name]
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if bool(other_field.data):
            super(RequiredIf, self).__call__(form, field)
        else:
            Optional().__call__(form, field)

class MainForm(FlaskForm):
	"""The form that contains all the options to generate a playbook"""
	#General
	playbook_name = StringField('Playbook name',default='playbook', validators=[Required('This field is required')])
	description = TextField('Description',default='')


	#Webservers section
	install_webserver = BooleanField('Install webserver', default=False)
	server_types = RadioField('Webserver type', choices=[('apache','Apache2'),('nginx','Nginx')], default='apache')
	document_root = StringField('Document root', validators=[RequiredIf('install_webserver')], default='/var/www/html')
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
	db_types = RadioField('Database management system', choices=[('mysql','MySQL'),('postgresql','PostgreSQL'),('sqlite','SQLite')], default='mysql')
	db_delete_anonymous = BooleanField('Delete anonymous user (MySQL)', default=False)
	db_delete_test = BooleanField('Delete test database (MySQL)', default=False)
	db_dir = StringField('SQLite directory', default='/var/lib/sqlite')
	db_create_db = BooleanField('Create database', default=False)
	db_name =  StringField('Database name', validators=[RequiredIf('db_create_db'), Length(message=u'Database name length must be in the range 3-20 characters', min=3, max=20)])
	db_create_user = BooleanField('Create user', default=False)
	db_username = StringField('Username', validators=[RequiredIf('db_create_user'), Length(message=u'Username length must be in the range 3-20 characters', min=3, max=20)])
	db_password = StringField('Password', validators=[RequiredIf('db_create_user'), Length(message=u'Password length must be in the range 6-20 characters', min=6, max=20)])


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

