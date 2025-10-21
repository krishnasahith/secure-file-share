#!/usr/bin/env python3
"""
Secure File Share - Cross-platform file sharing with authentication
Version: 3.0 (Modular)
Port: 8080 (avoids macOS AirPlay conflict on port 5000)
"""
import os
from flask import Flask
from flask_cors import CORS
from flask_session import Session

from config import Config
from utils import get_local_ip, generate_ascii_qr
from utils.connection import CONNECTION_CODE
from routes import main_bp, file_bp, auth_bp


def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    Session(app)
    CORS(app, supports_credentials=True)
    
    # Create uploads folder
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(file_bp)
    
    return app


def display_startup_info():
    """Display connection information on startup"""
    local_ip = get_local_ip()
    port = Config.PORT
    url = f"http://{local_ip}:{port}"
    
    print("\n" + "="*60)
    print("🔒 SECURE FILE SHARE SERVER")
    print("="*60)
    print(f"📡 Server running at: {url}")
    print(f"🔑 Connection Code: {CONNECTION_CODE}")
    print("="*60)
    print("\nScan QR Code to connect:")
    qr_url = f"{url}#code={CONNECTION_CODE}"
    print(generate_ascii_qr(qr_url))
    print("="*60)
    print(f"💡 Share the URL and Connection Code with devices")
    print(f"🛑 Press Ctrl+C to stop the server")
    print("="*60 + "\n")


if __name__ == '__main__':
    app = create_app()
    display_startup_info()
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
