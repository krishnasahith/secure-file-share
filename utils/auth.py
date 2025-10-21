"""
Authentication utilities
"""
import time
import secrets
import string
from functools import wraps
from flask import (
    jsonify, session, current_app, request,
    redirect, url_for, render_template
)


def generate_connection_code(length=8):
    """Generate cryptographically secure alphanumeric code"""
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def auth_required(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Allow only specific endpoints without authentication
        allowed_endpoints = ['static', 'auth.authenticate', 'auth.session_status']
        if request.endpoint not in allowed_endpoints:
            # Check if authenticated
            if not session.get('authenticated'):
                wants_json = (request.is_json or 
                            request.headers.get('Accept') == 'application/json' or 
                            request.path.startswith('/api/'))
                
                if wants_json:
                    return jsonify({
                        'error': 'Authentication required',
                        'code': 'AUTH_REQUIRED'
                    }), 401
                return render_template('index.html')
            
            # Check session expiration
            last_activity = session.get('last_activity', 0)
            session_lifetime = current_app.config['PERMANENT_SESSION_LIFETIME'].total_seconds()
            
            if time.time() - last_activity > session_lifetime:
                session.clear()
                if request.is_json:
                    return jsonify({
                        'error': 'Session expired',
                        'code': 'SESSION_EXPIRED'
                    }), 401
                return render_template('index.html')
            
            # Update last activity
            session['last_activity'] = time.time()
        
        return f(*args, **kwargs)
    
    return decorated_function
