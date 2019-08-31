import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


class Config(object):
    DEBUG = True
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
    DATABASE_USER = os.environ.get('DATABASE_USER')
    DATABASE_HOST = os.environ.get('DATABASE_HOST')
    DATABASE_NAME = os.environ.get('DATABASE_NAME')
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}/{}".format(DATABASE_USER, DATABASE_PASSWORD,
                                                                DATABASE_HOST, DATABASE_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    return app


rdb = redis.Redis(host=os.environ['REDIS_LOCATION'], port=os.environ['REDIS_PORT'], db=1)
