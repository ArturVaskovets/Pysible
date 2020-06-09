import os

SECRET_KEY = b'w\x17\xf10\x1a\xde\xab~\xb9\xd2\x04\xe5\xc0\x81\xd8\xdc'
PWD = os.path.abspath(os.curdir)
PROJECTS_DIR = '{}/user_projects/'.format(PWD)

DEBUG = False
SQLALCHEMY_DATABASE_URI = 'sqlite:////app/data.db'.format(PWD)
SQLALCHEMY_TRACK_MODIFICATIONS = False