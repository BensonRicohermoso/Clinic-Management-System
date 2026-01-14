# App configuration

import os
from datetime import timedelta

# Get the directory where this config file is located
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # base config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Use absolute path for database
    DATABASE = os.environ.get('DATABASE_PATH') or os.path.join(BASE_DIR, 'clinical_management.db')
    
    # File upload settings - use absolute path
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'lab_results')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    
    # session config
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Pagination
    ITEMS_PER_PAGE = 20
    
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