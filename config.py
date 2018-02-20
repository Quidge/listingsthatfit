import os
from helpers import get_env_variable

basedir = os.path.abspath(os.path.dirname(__file__))

PG_URL = get_env_variable('PGDATA')
PG_USER = get_env_variable('POSTGRES_USER')
PG_PASSWORD = get_env_variable('POSTGRES_PW')
PG_DB = get_env_variable('POSTGRES_DB')

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
	user=PG_USER, pw=PG_PASSWORD, url=PG_URL, db=PG_DB)
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')