import os
from typing import Optional

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or 'competency_database.db'
    
    # Flask configuration
    DEBUG = False
    TESTING = False
    
    # API configuration
    API_TITLE = 'Competency-Based Learning API'
    API_VERSION = '1.0.0'
    API_DESCRIPTION = 'REST API for managing competency-based learning system'
    
    # CORS configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Pagination
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    
    # Rate limiting (requests per minute)
    RATE_LIMIT = os.environ.get('RATE_LIMIT', '1000')
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'api.log')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    DATABASE_PATH = 'competency_database.db'
    CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000', 'http://localhost:5000']

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set in production")
    
    # Use environment-specific database path
    DATABASE_PATH = os.environ.get('DATABASE_PATH', '/var/lib/competency-api/database.db')
    
    # Stricter CORS for production
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',')
    if not CORS_ORIGINS or CORS_ORIGINS == ['']:
        raise ValueError("CORS_ORIGINS must be specified in production")

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DATABASE_PATH = ':memory:'  # Use in-memory database for testing
    SECRET_KEY = 'test-secret-key'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name: Optional[str] = None) -> Config:
    """Get configuration class based on environment"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    return config.get(config_name, config['default'])
