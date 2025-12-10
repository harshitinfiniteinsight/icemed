#!/usr/bin/env python3
"""
ICE Reconciliation Mock System - Run Script
Starts the Flask web application
"""

from web.app import app

if __name__ == '__main__':
    print("="*60)
    print("ICE Reconciliation Mock System")
    print("="*60)
    print("Server starting on http://localhost:5001")
    print("Open your browser and navigate to: http://localhost:5001")
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5001)
