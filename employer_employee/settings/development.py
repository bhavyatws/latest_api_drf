import os
from employer_employee.settings.common import *


DEBUG = True
if DEBUG:
        STATICFILES_DIRS = [
            os.path.join(BASE_DIR, 'static')
       ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

SECRET_KEY = 'django-insecure-0a_e8kpav*e3fkv2rn9^vsh6p*n^b@=9yh4yprq&m!8a--z4p&'

# SECURITY WARNING: update this when you have the production host
ALLOWED_HOSTS = ['*']