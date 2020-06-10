import os
from Pysible.app import app

SECRET_KEY = b'w\x17\xf10\x1a\xde\xab~\xb9\xd2\x04\xe5\xc0\x81\xd8\xdc'
PWD = os.path.normpath(app.root_path)
PROJECTS_DIR = os.path.join(PWD, 'user_projects/')
APP_UID = os.stat(os.path.join(PWD, 'app.py')).st_uid # Get application owners uid
APP_GID = os.stat(os.path.join(PWD, 'app.py')).st_gid # Get application owners uid

DEBUG = False
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:{}@{}/pysible'.format(os.environ["MYSQL_PASSWORD"],os.environ["MYSQL_PORT_3306_TCP_ADDR"])
SQLALCHEMY_TRACK_MODIFICATIONS = False
