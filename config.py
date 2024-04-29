"""Contains the Application Configuration Parameters"""
# https://realpython.com/flask-blueprint/

import os
#from dotenv import load_dotenv, find_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    FLASK_APP = 'app.py'
    #FLASK_ENV = 'development'
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    UNITED_MAIL_SUBJECT_PREFIX = '[Online Enquiry]'
    UNITED_MAIL_SENDER = 'United Admin <pythonapi2023@gmail.com>'
    PORT = int(os.getenv('PORT', 4242))  # This is needed to deploy on fl0

    @staticmethod
    def init_app(app):
        pass

