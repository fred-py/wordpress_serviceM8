import os

basedir = os.path.abspath(os.path.dirname(__file__))

url = os.getenv('FL0_URL')


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False