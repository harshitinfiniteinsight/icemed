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

# Import Flask app
from web.app import app

# Vercel Python runtime expects the WSGI app directly
# Export as both 'handler' and 'app' for compatibility
handler = app
