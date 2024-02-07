"""Contains the Application Configuration Parameters"""
# https://realpython.com/flask-blueprint/

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    FLASK_APP = 'app.py'
    #FLASK_ENV = 'development'
