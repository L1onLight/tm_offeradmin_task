from .base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DB_NAME_DEV"),
        "USER": os.getenv("DB_USER_DEV"),
        "PASSWORD": os.getenv("DB_PASSWORD_DEV"),
        "HOST": os.getenv("DB_HOST_DEV"),
        "PORT": os.getenv("DB_PORT_DEV"),
    }
}


ALLOWED_HOSTS = [
    "mb30host.online",
    "www.mb30host.online",
    "localhost",
    "www.localhost",
    "127.0.0.1",
]
