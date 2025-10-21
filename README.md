# Secure File Share

A simple local network file sharing application built with Flask.

## Features

- Secure authentication using 6-digit connection codes.
- File upload and download capabilities.
- Responsive design for both desktop and mobile.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/file-share-app.git
   cd file-share-app
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv fileproject
   source fileproject/bin/activate  # For Windows: fileproject\Scripts\activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the server:

   ```bash
   python app.py
   ```

## Project Structure

```
file-share-app/
├── app.py              # Main application entry point
├── config.py           # Configuration settings
├── models.py           # Data models (e.g., file metadata)
├── requirements.txt    # Python dependencies
├── routes/            # Flask blueprints
│   ├── __init__.py
│   ├── auth_routes.py  # Authentication endpoints
│   ├── file_routes.py  # File management endpoints
│   └── main_routes.py  # Main page routes
├── static/            # Static assets (CSS, JS files)
├── templates/         # HTML templates (front-end)
└── utils/             # Utility modules (authentication, connection, file handling, network)
```

## Usage

- **Connect:** Open the local network URL displayed when the server starts and enter the provided 6-digit connection code.
- **Upload:** Use the web interface to upload files.
- **Download/Delete:** Download files or delete your own uploads as needed.

## License

MIT License
