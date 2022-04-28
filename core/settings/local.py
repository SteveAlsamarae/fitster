from .base import *

from pathlib import Path

# Build paths : BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += [
    "django_extensions",
    "debug_toolbar",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INTERNAL_IPS = [
    "127.0.0.1",
]

SHELL_PLUS = "ipython"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

LOGGING["loggers"] = {
    "werkzeug": {
        "handlers": ["console"],
        "level": "DEBUG",
        "propagate": True,
    },
}
