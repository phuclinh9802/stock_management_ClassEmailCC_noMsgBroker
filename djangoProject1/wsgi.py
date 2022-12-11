
"""
WSGI config for djangoProject1 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject1.settings')

project_folder = os.path.expanduser('~/group3sprint.pythonanywhere.com')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))
application = get_wsgi_application()
