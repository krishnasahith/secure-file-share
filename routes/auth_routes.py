"""
Authentication routes
"""
import time
from flask import Blueprint, request, jsonify, session, current_app
from config import Config
from utils.connection import CONNECTION_CODE

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/authenticate', methods=['POST'])
def authenticate():
    """Authenticate connection code"""
    data = request.get_json()
    provided_code = data.get('code', '').strip().upper()
    
    # Check rate limiting
    attempts = session.get('auth_attempts', 0)
    lockout_until = session.get('lockout_until', 0)
    
    if attempts >= current_app.config.get('MAX_AUTH_ATTEMPTS', 5) and time.time() < lockout_until:
        return jsonify({
            'success': False,
            'error': 'Too many attempts',
            'retry_after': int(lockout_until - time.time())
        }), 429
    
    # Reset lockout if time has passed
    if time.time() >= lockout_until:
        session['auth_attempts'] = 0
    
    # Get the connection code from app
    from app import CONNECTION_CODE
    
    if provided_code == CONNECTION_CODE:
        session['authenticated'] = True
        session['auth_attempts'] = 0
        session['last_activity'] = time.time()
        session.permanent = True
        print(f"✓ Successful authentication from {request.remote_addr}")
        return jsonify({'success': True, 'message': 'Authentication successful'})
    else:
        attempts = session.get('auth_attempts', 0) + 1
        session['auth_attempts'] = attempts
        
        if attempts >= current_app.config.get('MAX_AUTH_ATTEMPTS', 5):
            lockout_duration = current_app.config.get('LOCKOUT_DURATION', 300)  # 5 minutes default
            session['lockout_until'] = time.time() + lockout_duration
            print(f"✗ Authentication locked out for {request.remote_addr}")
            return jsonify({
                'success': False,
                'error': 'Too many attempts',
                'retry_after': lockout_duration
            }), 429
        
        print(f"✗ Failed authentication attempt from {request.remote_addr} (Attempt {attempts})")
        return jsonify({
            'success': False,
            'error': 'Invalid code',
            'attempts_remaining': current_app.config.get('MAX_AUTH_ATTEMPTS', 5) - attempts
        }), 401


@auth_bp.route('/disconnect', methods=['POST'])
def disconnect():
    """Disconnect and clear session"""
    session.clear()
    return jsonify({'success': True, 'message': 'Disconnected successfully'})


@auth_bp.route('/session-status', methods=['GET'])
def session_status():
    """Check if session is authenticated"""
    is_authenticated = session.get('authenticated', False)
    
    if is_authenticated:
        last_activity = session.get('last_activity', 0)
        session_lifetime = current_app.config['PERMANENT_SESSION_LIFETIME'].total_seconds()
        
        if time.time() - last_activity > session_lifetime:
            session.clear()
            return jsonify({
                'authenticated': False,
                'error': 'Session expired'
            })
        
        # Update last activity
        session['last_activity'] = time.time()
        return jsonify({
            'authenticated': True,
            'connection_code_hint': CONNECTION_CODE[:4] + '****',
            'expires_in': int(session_lifetime - (time.time() - last_activity))
        })
    
    return jsonify({
        'authenticated': False,
        'error': 'Not authenticated'
    })
