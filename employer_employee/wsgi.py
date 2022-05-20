"""
WSGI config for employer_employee project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""
import os
from django.core.wsgi import get_wsgi_application
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent.parent


# from whitenoise import WhiteNoise


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "employer_employee.settings.development"
)
application = get_wsgi_application()

# application = WhiteNoise(application)
