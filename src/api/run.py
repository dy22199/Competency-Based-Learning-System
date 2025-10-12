#!/usr/bin/env python3
"""
Main entry point for the Competency-Based Learning API
"""

import os
import sys
from flask import Flask

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import get_config

def create_app(config_name=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    
    # Import and register blueprints
    from app import app as api_app
    
    # Copy routes from api_app to main app
    for rule in api_app.url_map.iter_rules():
        app.add_url_rule(
            rule.rule,
            endpoint=rule.endpoint,
            view_func=api_app.view_functions[rule.endpoint],
            methods=rule.methods
        )
    
    return app

if __name__ == '__main__':
    # Get configuration from environment
    config_name = os.environ.get('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    # Get host and port from environment
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = app.config.get('DEBUG', False)
    
    print(f"Starting Competency-Based Learning API")
    print(f"Environment: {config_name}")
    print(f"Debug mode: {debug}")
    print(f"Database: {app.config.get('DATABASE_PATH')}")
    print(f"Server: http://{host}:{port}")
    
    app.run(host=host, port=port, debug=debug)
