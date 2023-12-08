

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
settings_module = 'azure_project.deployment' if 'WEBSITE_HOSTNAME' in os.environ else ''
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'udemyclone.settings')

application = get_wsgi_application()
application = WhiteNoise(application)