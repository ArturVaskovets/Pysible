import click # pylint: disable=import-error
from flask import Blueprint # pylint: disable=import-error
from Pysible.app import db
from Pysible.models import Templates, Users
import json

bpdatabase = Blueprint('bpdatabase', __name__, cli_group="db")

@bpdatabase.cli.command('create')
@click.option('-w', '--with_data', is_flag=True, help='Import data once created.')
@click.pass_context
def create(ctx, with_data=False):
	"Create relational database tables."
	db.create_all()
	if with_data:
		ctx.invoke(add_data)

@bpdatabase.cli.command('drop')
def drop():
	"Drop all project relational database tables with data"
	db.drop_all()

@bpdatabase.cli.command('recreate')
def recreate():
	"Recreate all the tables in case you have changed the model"
	db.drop_all()
	db.create_all()

@bpdatabase.cli.command('add_data')
def add_data():
	"Add test data to the model"
	with open('test_users.json') as json_file:
		users = json.load(json_file)
		for user in users:
			us=Users(**user)
			db.session.add(us)
			db.session.commit()

@bpdatabase.cli.command('import_templates')
def import_templates():
	"Import ansible templates from file"
	with open('templates.json') as json_file:
		data = json.load(json_file)
		for key,value in data.items():
			template = Templates(id=key, text=value)
			db.session.add(template)
			db.session.commit()

@bpdatabase.cli.command('set_admin')
def set_admin():
	"Create test admin. Don't use in production."
	pass

@bpdatabase.cli.command('wipe')
def wipe():
	"Remove the data but not model"
	pass

@bpdatabase.cli.command('print_all')
def print_all():
	"Print all data in the table"
	pass


bpflask = Blueprint('bpflask', __name__, cli_group=None)
@bpflask.cli.command('init_app')
@click.option('-d', '--debug', is_flag=True, help='Import data for tests')
@click.pass_context
def init_app(ctx, debug):
	"Do all necessary work to run the app: create database, import templates, etc."
	db.drop_all()
	ctx.invoke(create, with_data=debug)
	ctx.invoke(import_templates)