import os

class Config(object):
    SECRET_KEY = 'my secret key'
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///dumme.db'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://devuser:7aVY2qgou5Dc@192.168.178.2:5433/racketservice-dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False