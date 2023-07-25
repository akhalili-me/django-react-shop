from .base import *
import os 
from dotenv import load_dotenv

load_dotenv()

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": "db",
        "PORT": "5432",
    }
}

# INSTALLED_APPS += ['debug_toolbar',]