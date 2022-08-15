from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    FLASK_APP = environ.get("FLASK_APP")
    SECRET_KEY = environ.get('SECRET_KEY')
#    SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    FLASK_DEBUG = 1
    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URI')
    POSTS_PER_PAGE = 5

class ProdConfig(Config):
    FLASK_DEBUG = 0
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = environ.get('PROD_DATABASE_URI')

class DevConfig(Config):
    FLASK_DEBUG = 1
    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URI')