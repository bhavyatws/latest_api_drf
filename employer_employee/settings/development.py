import os
from employer_employee.settings.common import *
from dotenv import load_dotenv
load_dotenv() 

DEBUG = True

SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: update this when you have the production host
ALLOWED_HOSTS = ['*']