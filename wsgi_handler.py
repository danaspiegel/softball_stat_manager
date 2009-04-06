import os, sys

sys.stdout = sys.stderr

# Calculate the path based on the location of the WSGI script.
project = os.path.dirname(__file__)
sys.path.append(project)

os.environ['PYTHON_EGG_CACHE'] = '/home/.python-eggs'
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
