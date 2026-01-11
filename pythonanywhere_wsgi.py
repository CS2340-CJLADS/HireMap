"""
PythonAnywhere WSGI Configuration File
Copy this content to your PythonAnywhere WSGI configuration file
(Web tab -> WSGI configuration file)

IMPORTANT: Replace 'yourusername' with your actual PythonAnywhere username
and 'hiremap' with your actual project directory name if different.
"""

import os
import sys

# Add your project directory to the Python path
path = '/home/yourusername/hiremap'
if path not in sys.path:
    sys.path.insert(0, path)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'HireMap.settings'

# Activate your virtual environment
activate_this = '/home/yourusername/hiremap/venv/bin/activate_this.py'
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()



