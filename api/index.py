"""
Vercel serverless function entry point
"""
import sys
import os

# Add parent directory to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

# Change to project root for file paths to work correctly
os.chdir(PROJECT_ROOT)

try:
    from web.app import app
    
    # Export app for Vercel (Vercel looks for 'handler' or 'app')
    handler = app
    
except Exception as e:
    # Create a minimal error handler if app fails to load
    from flask import Flask, jsonify
    
    error_app = Flask(__name__)
    
    @error_app.route('/')
    @error_app.route('/<path:path>')
    def error_handler(path=''):
        return jsonify({
            'error': 'Application failed to initialize',
            'message': str(e),
            'project_root': PROJECT_ROOT
        }), 500
    
    handler = error_app
