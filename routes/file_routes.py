"""
File management routes
"""
import os
from flask import Blueprint, request, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename
from utils import auth_required, allowed_file

file_bp = Blueprint('file', __name__)


@file_bp.route('/upload', methods=['POST'])
@auth_required
def upload_file():
    """Handle file upload with chunking support"""
    # Check if any file was sent
    if len(request.files) == 0:
        return jsonify({'error': 'No file was sent'}), 400
    
    # Check for the file field specifically
    if 'file' not in request.files:
        return jsonify({'error': 'File must be sent with field name "file"'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    # For chunked upload
    original_filename = request.form.get('filename', file.filename)
    chunk_number = request.form.get('chunk')
    total_chunks = request.form.get('chunks')
    
    if original_filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(original_filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    filename = secure_filename(original_filename)
    upload_folder = current_app.config['UPLOAD_FOLDER']
    
    # Handle chunked upload
    if chunk_number is not None and total_chunks is not None:
        chunk_number = int(chunk_number)
        total_chunks = int(total_chunks)
        
        # Create temp directory for chunks if it doesn't exist
        temp_dir = os.path.join(upload_folder, '.temp')
        os.makedirs(temp_dir, exist_ok=True)
        
        # Create directory for this file's chunks
        file_temp_dir = os.path.join(temp_dir, filename)
        os.makedirs(file_temp_dir, exist_ok=True)
        
        # Save the chunk
        chunk_path = os.path.join(file_temp_dir, f'chunk_{chunk_number}')
        file.save(chunk_path)
        
        # If this is the final chunk, combine all chunks
        if chunk_number == total_chunks - 1:
            try:
                final_path = os.path.join(upload_folder, filename)
                
                # Handle duplicate filenames
                base, ext = os.path.splitext(filename)
                counter = 1
                while os.path.exists(final_path):
                    filename = f"{base}_{counter}{ext}"
                    final_path = os.path.join(upload_folder, filename)
                    counter += 1
                
                # Combine chunks
                with open(final_path, 'wb') as outfile:
                    for i in range(total_chunks):
                        chunk_file = os.path.join(file_temp_dir, f'chunk_{i}')
                        with open(chunk_file, 'rb') as infile:
                            outfile.write(infile.read())
                
                # Clean up temp directory
                import shutil
                shutil.rmtree(file_temp_dir)
                
                # Clean up temp dir if empty
                if not os.listdir(temp_dir):
                    os.rmdir(temp_dir)
                
                return jsonify({
                    'success': True,
                    'message': 'File uploaded successfully',
                    'filename': filename,
                    'size': os.path.getsize(final_path)
                })
            except Exception as e:
                # Clean up temp files in case of error
                if os.path.exists(file_temp_dir):
                    shutil.rmtree(file_temp_dir)
                return jsonify({'error': f'Upload failed: {str(e)}'}), 500
        
        return jsonify({'success': True, 'message': 'Chunk received'})
    
    # Handle regular upload (no chunking)
    try:
        final_path = os.path.join(upload_folder, filename)
        
        # Handle duplicate filenames
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(final_path):
            filename = f"{base}_{counter}{ext}"
            final_path = os.path.join(upload_folder, filename)
            counter += 1
        
        file.save(final_path)
        
        return jsonify({
            'success': True,
            'message': 'File uploaded successfully',
            'filename': filename,
            'size': os.path.getsize(final_path)
        })
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500


@file_bp.route('/files', methods=['GET'])
@auth_required
def list_files():
    """List all uploaded files"""
    upload_folder = current_app.config['UPLOAD_FOLDER']
    
    if not os.path.exists(upload_folder):
        return jsonify({'files': []})
    
    files = []
    for filename in os.listdir(upload_folder):
        filepath = os.path.join(upload_folder, filename)
        if os.path.isfile(filepath):
            files.append({
                'name': filename,
                'size': os.path.getsize(filepath),
                'modified': os.path.getmtime(filepath)
            })
    
    # Sort by modification time (newest first)
    files.sort(key=lambda x: x['modified'], reverse=True)
    
    return jsonify({'files': files})


@file_bp.route('/download/<filename>', methods=['GET'])
@auth_required
def download_file(filename):
    """Download a file"""
    try:
        return send_from_directory(
            current_app.config['UPLOAD_FOLDER'],
            filename,
            as_attachment=True
        )
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404


@file_bp.route('/delete/<filename>', methods=['DELETE'])
@auth_required
def delete_file(filename):
    """Delete a file"""
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    try:
        os.remove(filepath)
        return jsonify({'success': True, 'message': 'File deleted successfully'})
    except Exception as e:
        return jsonify({'error': f'Delete failed: {str(e)}'}), 500
