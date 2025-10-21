"""
Configuration settings for Secure File Share application
"""
import os
import secrets
from datetime import timedelta

class Config:
    """Base configuration"""
    # Flask settings
    SECRET_KEY = secrets.token_hex(32)
    
    # Session settings
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    
    # File upload settings
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB max file size
    CHUNK_SIZE = 1024 * 1024  # 1MB chunk size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {
        'pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt',
        'jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg',
        'mp4', 'avi', 'mov', 'mkv',
        'mp3', 'wav', 'flac',
        'zip', 'rar', '7z', 'tar', 'gz',
        'apk'
    }
    
    # Server settings
    HOST = '0.0.0.0'
    PORT = 8080
    DEBUG = False
    
    # Security settings
    CONNECTION_CODE_LENGTH = 8
    MAX_AUTH_ATTEMPTS = 5
    LOCKOUT_DURATION = 300  # 5 minutes
    
    # Cleanup settings
    FILE_EXPIRY_DAYS = 7  # Auto-delete files after 7 days
    SESSION_CLEANUP_INTERVAL = 3600  # Clean expired sessions every hour
    FILE_CLEANUP_INTERVAL = 86400  # Clean old files every day
    
    # Rate limiting settings
    RATELIMIT_DEFAULT = "200 per day"
    RATELIMIT_STORAGE_URL = "memory://"
