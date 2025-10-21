"""
Main application routes
"""
from flask import Blueprint, render_template, session, jsonify
from utils.auth import auth_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@auth_required
def index():
    """Serve main page"""
    return render_template('index.html')
