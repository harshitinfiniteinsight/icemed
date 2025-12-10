"""
Vercel serverless function entry point
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from web.app import app

# Vercel will use this 'app' variable
app = app
