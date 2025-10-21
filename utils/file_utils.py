"""
File handling utilities
"""
from flask import current_app


def allowed_file(filename):
    """Check if file extension is allowed"""
    if '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()  # Fix: get second part of split
    return extension in current_app.config['ALLOWED_EXTENSIONS']
