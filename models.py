from sqlalchemy import Column, Integer, String, Boolean, ForeignKey # pylint: disable=import-error
from sqlalchemy.orm import relationship # pylint: disable=import-error
from werkzeug.security import generate_password_hash, check_password_hash # pylint: disable=import-error
from main import db

class Templates(db.Model):
	"""Ansible task templates"""
	__tablename__ = 'templates'
	id = Column(String(100), primary_key = True, nullable=False)
	text = Column(String(1000), nullable=False) 

class Projects(db.Model):
	"""Projects of each user"""
	__tablename__ = 'projects'
	id = Column(Integer, primary_key=True)
	name = Column(String(100),nullable=False)
	description = Column(String(255))
	user_id = Column(Integer,ForeignKey('users.id') ,nullable=False)
	user = relationship("Users", backref="Projects")

class Users(db.Model):
	"""Users and admins"""
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	username = Column(String(100),nullable=False)
	password_hash = Column(String(128),nullable=False)
	name = Column(String(200),nullable=False)
	email = Column(String(200))
	admin = Column(Boolean, default=False)

	def __repr__(self):
		return """User - {}
		Username - {},
		Name - {},
		Email - {},
		Status - {}""".format(
			self.id,
			self.username,
			self.name,
			self.email,
			"admin" if self.admin else "user"
		)

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

# Flask-Login integration
	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.id)

	def is_admin(self):
		return self.admin