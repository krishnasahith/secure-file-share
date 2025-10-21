"""
Route blueprints for Secure File Share application
"""
from .main_routes import main_bp
from .file_routes import file_bp
from .auth_routes import auth_bp

__all__ = ['main_bp', 'file_bp', 'auth_bp']
