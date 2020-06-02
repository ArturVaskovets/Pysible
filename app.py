from flask import Flask, render_template, render_template_string, Response, abort, redirect, url_for, request,send_from_directory # pylint: disable=import-error
from flask_bootstrap import Bootstrap # pylint: disable=import-error
from flask_sqlalchemy import SQLAlchemy # pylint: disable=import-error
from flask_login import LoginManager, login_user, logout_user, login_required,	current_user # pylint: disable=import-error
from Pysible import config
from Pysible.forms import MainForm, LoginForm, SignupForm, AccountEditForm
import os
import shutil

app = Flask(__name__)
app.config.from_object(config)
Bootstrap(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from Pysible.cli import bpdatabase, bpflask
app.register_blueprint(bpdatabase)
app.register_blueprint(bpflask)
from Pysible.models import Templates, Users, Projects

@app.route('/', methods=["get","post"])
def start():
	form = MainForm()
	if form.validate_on_submit():
		playbook = generatePlaybook(form)
		generator = (cell for row in playbook for cell in row)
		return Response(generator, mimetype="text/plain",headers={"Content-Disposition":"attachment;filename={}.yaml".format(form.playbook_name.data)})
	else:
		return render_template('home.html', form=form)

@app.route('/save', methods=["post"])
@login_required
def save():
	form = MainForm()
	if form.validate_on_submit():
		path = app.config["PROJECTS_DIR"] + Users.query.get(current_user.id).username + "/"
		filename = form.playbook_name.data + ".yaml"

		#Potential errors
		if not os.path.exists(path):
			os.makedirs(path)
		if os.path.isfile(path + filename):
			form.playbook_name.errors.append("File exists")
			return render_template('home.html', form=form)

		#Write file
		playbook = generatePlaybook(form)
		with open(path + filename, "w") as f:
			f.write(playbook)

		#Add project to database
		project = Projects(name=form.playbook_name.data,description=form.description.data,user_id=current_user.id)
		db.session.add(project)
		db.session.commit()


		return redirect(url_for("projects"))
	else:
		return render_template('home.html', form=form)

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/users')
@login_required
def users():
	if not current_user.is_admin(): # Only admins can access here
		abort(403)

	users = Users.query.all()
	return render_template('users.html', users=users)

@app.route('/user_delete/<username>')
@login_required
def user_delete(username):
	if current_user.username == username or not current_user.is_admin(): # Only admins can delete users but can't delete themselves
		abort(403)

	user = Users.query.filter_by(username=username).first()
	if user is None:
		abort(404)

	projects = Projects.query.filter_by(user_id=user.id)
	for project in projects:
		db.session.delete(project)
		db.session.commit()
	
	db.session.delete(user)
	db.session.commit()

	path = app.config["PROJECTS_DIR"] + username + "/"
	if os.path.exists(path):
		shutil.rmtree(path)

	return redirect(url_for("users"))

@app.route('/account')
@app.route('/account/<username>')
@login_required
def account(username = None):
	form = AccountEditForm()
	if username is None:
		username = current_user.username

	if current_user.username != username and not current_user.is_admin(): # Only owner and admins can access here
		abort(403)

	user = Users.query.filter_by(username=username).first()
	if user is None:
		abort(404)

	form.username.data = user.username
	form.name.data = user.name
	form.email.data = user.email

	return render_template('account.html', form=form, username=username)

@app.route('/account_edit/<username>', methods=["post"]) # Adapted both for users and for admins
@login_required
def account_edit(username):
	if current_user.username != username and not current_user.is_admin(): # Only owner and admins can change account
		abort(403)

	form = AccountEditForm()
	user = Users.query.filter_by(username=username).first()
	if user is None:
		abort(404)

	if form.validate_on_submit(): # For security reasons admin status can be set only with 'set_admin' cli command
		user.name = form.name.data
		user.email = form.email.data
		if form.password.data != '':
			user.password = form.password.data
		db.session.commit()
	else:
		abort(500)

	return redirect(url_for("start"))

@app.route('/login', methods=["get","post"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("start"))

	form = LoginForm()
	if form.validate_on_submit():
		user=Users.query.filter_by(username=form.username.data).first()
		if user!=None and user.verify_password(form.password.data):
			login_user(user)
			next = request.args.get('next')
			return redirect(next or url_for('start'))
		else:
			form.username.errors.append("Username or password are incorrect")
	return render_template('login.html', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route('/signup', methods=["get","post"])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for("start"))

	form = SignupForm()
	if form.validate_on_submit():
		user=Users.query.filter_by(username=form.username.data).first()
		if user==None:
			#Database
			user = Users()
			form.populate_obj(user)
			db.session.add(user)
			db.session.commit()

			#File system
			path = app.config["PROJECTS_DIR"] + user.username + "/"
			if os.path.exists(path):
				shutil.rmtree(path)
			os.makedirs(path)

			login_user(user)
			return redirect(url_for('start'))
		else:
			form.username.errors.append("User exists")
	return render_template('signup.html', form=form)

@app.route('/projects')
@app.route('/projects/<username>')
@login_required
def projects(username = None):
	if username is None:
		username = current_user.username

	if current_user.username != username and not current_user.is_admin(): # Only owner and admins can access here
		abort(403)
	
	user = Users.query.filter_by(username=username).first()
	if user is None:
		abort(404)

	projects = Projects.query.filter_by(user_id=user.id)
	return render_template('projects.html', projects=projects, username=username)

@app.route('/project_download/<username>/<name>')
@login_required
def project_download(username, name):
	if current_user.username != username and not current_user.is_admin(): # Only owner and admins can download the project
		abort(403)

	path = app.config["PROJECTS_DIR"] + username + "/"
	filename = name + ".yaml"

	if not os.path.isfile(path + filename):
		abort(404)

	return send_from_directory(directory=path, filename=filename, as_attachment=True)

@app.route('/project_delete/<username>/<name>')
@login_required
def project_delete(username, name):
	if current_user.username != username and not current_user.is_admin(): # Only owner and admins can delete the project
		abort(403)

	user = Users.query.filter_by(username=username).first()
	if user is None:
		abort(404)

	path = app.config["PROJECTS_DIR"] + username + "/"
	filename = name + ".yaml"

	if not os.path.isfile(path + filename):
		abort(404)
		
	os.remove(path + filename)

	project = Projects.query.filter_by(user_id=user.id, name=name).first()
	db.session.delete(project)
	db.session.commit()

	return redirect(url_for("projects", username=username))

@app.route('/project_share/<username>/<name>')
@login_required
def project_share(username, name):
	return redirect(url_for("projects", username=username))

@app.route('/tests')
def tests():
	return render_template('tests.html')

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))

def generatePlaybook(form):
	try:
		#General
		playbook = Templates.query.get('base').text
		tasks = Templates.query.get('tasks').text
		handlers = Templates.query.get('handlers').text


		#Webservers
		if form.install_webserver.data:
			if form.server_types.data == 'apache':
				temp = Templates.query.get('apache_tasks').text
				handlers += Templates.query.get('apache_handlers').text
			else:
				temp = Templates.query.get('nginx_tasks').text
				handlers += Templates.query.get('nginx_handlers').text
			tasks += render_template_string(temp, document_root=form.document_root.data, server_name=form.server_name.data)


		#Interpreters
		#PHP
		if form.install_php.data:
			temp = Templates.query.get('php_tasks').text
			tasks += render_template_string(temp, version=form.version_php.data)
		
		#Python
		if form.install_python.data:
			temp = Templates.query.get('python_tasks').text
			tasks += render_template_string(temp, version=form.version_python.data)
	except:
		abort(500)
	
	playbook = playbook + tasks + handlers
	return playbook