import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '311296'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    GIT_ACCESS_TOKEN = '3ec41628d6ba0c12e528628ddad7705b45419676'
    GIT_API_BASE_URL = 'https://api.github.com'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True