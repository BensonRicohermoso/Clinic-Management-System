# App configuration

import os
from datetime import timedelta

class Config:
    # base config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    DATABASE = os.environ.get('DATABASE_PATH') or 'clinical_management.db'
    
    # session config
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    APP_NAME = 'Clinical Management System'
    APP_VERSION = '1.0.0'
    
class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True  # needs HTTPS

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE = ':memory:'  # in-memory db for tests

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}