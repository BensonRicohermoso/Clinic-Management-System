# Production runner for the app

import os
import sys
from app import app

def check_environment():
    print("Clinical Management System")
    print("Starting up...\n")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or higher is required!")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    
    print(f"✓ Python version: {sys.version.split()[0]}")
    
    db_path = app.config['DATABASE']
    if os.path.exists(db_path):
        print(f"Database: {db_path}")
    else:
        print(f"Will create database: {db_path}")
    
    if not os.path.exists('templates'):
        print("ERROR: Templates folder not found!")
        sys.exit(1)
    print("Templates OK\n")

def main():
    check_environment()
    
    app.config['DEBUG'] = False
    app.config['TESTING'] = False
    
    host = os.environ.get('CMS_HOST', '0.0.0.0')
    port = int(os.environ.get('CMS_PORT', 5001))  # Changed to 5001 for macOS Monterey+ compatibility
    
    print(f"Starting server on http://{host}:{port}")
    print("Press CTRL+C to stop\n")
    
    try:
        app.run(host=host, port=port, debug=False)
    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()