import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///default.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') or False
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or r'C:\hugov\images_hub_venda'
    ALLOWS_IMAGES_STORE_DATABASE = os.environ.get('ALLOWS_IMAGES_STORE_DATABASE') or False

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True