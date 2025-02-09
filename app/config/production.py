from pathlib import Path
from datetime import timedelta

from .env_reader import env, csv

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = env("SECRET_KEY")
DATABASE_URL = env("DATABASE_URL")
ALLOWED_HOSTS = env("ALLOWED_HOSTS", cast=csv())
DEBUG = env("DEBUG", cast=bool)



# Database
DATABASES = {
    'default': dj_database_url.config(default=DATABASE_URL)
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "AUTH_HEADER_TYPES": ("Bearer",),
}