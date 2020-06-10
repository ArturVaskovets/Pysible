import os
from Pysible.main import app

SECRET_KEY = b'w\x17\xf10\x1a\xde\xab~\xb9\xd2\x04\xe5\xc0\x81\xd8\xdc'
PWD = os.path.normpath(app.root_path)
PROJECTS_DIR = os.path.join(PWD, 'user_projects/')
APP_UID = os.stat(os.path.join(PWD, 'main.py')).st_uid # Get application owners uid
APP_GID = os.stat(os.path.join(PWD, 'main.py')).st_gid # Get application owners uid

DEBUG = False
db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = '/cloudsql/' + str(os.environ.get('CLOUD_SQL_CONNECTION_NAME'))
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}?unix_socket={}'.format(db_user, db_password, db_name, db_connection_name)
SQLALCHEMY_TRACK_MODIFICATIONS = False
