import os
import glob
import streamlit as st
import re

def init_session_state():
    """
    Initializes session state variables to prevent errors when 
    accessing keys that haven't been set yet.
    """
    defaults = {
        'ids': [],
        'last_file': None,
        'params': [],
        'extraction_running': False
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

def get_out_files(directory):
    """
    Scans a directory for .out files. 
    Returns a sorted list of full file paths.
    """
    if not os.path.isdir(directory):
        return []
    
    # Use glob to find .out files (case insensitive if possible, but keeping simple here)
    files = glob.glob(os.path.join(directory, "*.out"))
    return sorted(files)

def format_file_size(filepath):
    """
    Returns a human-readable file size (e.g., '1.2 GB').
    Useful for warning users before processing massive files.
    """
    try:
        size = os.path.getsize(filepath)
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
    except Exception:
        return "Unknown size"
    return "Unknown size"

def sanitize_filename(name):
    """
    Removes invalid characters from a string to make it safe for filenames.
    Preserves alphanumeric characters, underscores, and hyphens.
    """
    # Replace common invalid characters with underscores
    name = str(name)
    name = re.sub(r'[<>:"/\\|?*]', '_', name) 
    return name.strip()

def get_subdirectories(path):
    """
    Returns a list of immediate subdirectories for navigation.
    """
    try:
        return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    except PermissionError:
        return []
    except FileNotFoundError:
        return []
