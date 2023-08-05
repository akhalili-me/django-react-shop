from .base import *

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": get_env_variable("DB_NAME"),
        "USER": get_env_variable("DB_USER"),
        "PASSWORD": get_env_variable("DB_PASSWORD"),
        "HOST": get_env_variable("DB_HOST"),
        "PORT": "5432",
    }
}
