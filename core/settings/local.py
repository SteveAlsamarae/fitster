
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

# Stripe settings
try:
    STRIPE_LIVE_SECRET_KEY = env("STRIPE_LIVE_SECRET_KEY")
    STRIPE_TEST_SECRET_KEY = env("STRIPE_TEST_SECRET_KEY")
    STRIPE_PUBLIC_KEY = env("STRIPE_PUBLIC_KEY")
    DJSTRIPE_WEBHOOK_SECRET = env("DJSTRIPE_WEBHOOK_SECRET")
    STRIPE_LIVE_MODE = bool(env("STRIPE_LIVE_MODE"))
    DJSTRIPE_FOREIGN_KEY_TO_FIELD = env("DJSTRIPE_FOREIGN_KEY_TO_FIELD")
    DJSTRIPE_USE_NATIVE_JSONFIELD = True

except Exception as excep:
    STRIPE_LIVE_SECRET_KEY = os.environ.get("STRIPE_LIVE_SECRET_KEY", "live_secret_key")
    STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY", "test_secret_key")
    STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY", "public_key")
    DJSTRIPE_WEBHOOK_SECRET = os.environ.get("DJSTRIPE_WEBHOOK_SECRET", "wh_secret")
    STRIPE_LIVE_MODE = os.environ.get("STRIPE_LIVE_MODE", False)
    DJSTRIPE_FOREIGN_KEY_TO_FIELD = os.environ.get("DJSTRIPE_FOREIGN_KEY_TO_FIELD", "id")
    DJSTRIPE_USE_NATIVE_JSONFIELD = True

    raise ImproperlyConfigured("Stripe settings are not configured properly", excep)

LOGGING["loggers"] = {
    "werkzeug": {
        "handlers": ["console"],
        "level": "DEBUG",
        "propagate": True,
    },
}
