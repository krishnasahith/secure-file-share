"""
Network utilities
"""
import socket
import qrcode
from io import StringIO


def get_local_ip():
    """Get local network IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)  # Set timeout to avoid hanging
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]  # Get only the IP address
        s.close()
        return local_ip
    except Exception:
        # Try alternative method if the first one fails
        try:
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)
        except Exception:
            return "127.0.0.1"


def generate_ascii_qr(url):
    """Generate ASCII art QR code for a URL
    
    Args:
        url (str): URL to encode (can include auth code as hash fragment)
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=1,
    )
    
    qr.add_data(url)
    qr.make(fit=True)
    
    # Generate ASCII QR code
    output = StringIO()
    qr.print_ascii(out=output, invert=True)
    return output.getvalue()
