"""
Connection code management
"""
from utils.auth import generate_connection_code
from config import Config

# Generate and store connection code
CONNECTION_CODE = generate_connection_code(Config.CONNECTION_CODE_LENGTH)