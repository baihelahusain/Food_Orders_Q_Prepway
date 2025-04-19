"""
WSGI config for foodsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Check if running on Render
if os.environ.get('RENDER', False):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foodsite.settings_render")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foodsite.settings")

application = get_wsgi_application()
