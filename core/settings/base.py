import os
from pathlib import Path

import environ
from django.core.exceptions import ImproperlyConfigured

# Build paths : BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()

# Take environment variables from .env file
env.read_env(BASE_DIR / ".env")

# False if not in os.environ because of casting above
try:
    DEBUG = env("DEBUG")
except ImproperlyConfigured:
    DEBUG = os.environ.get("DEBUG")

# Raises Django's ImproperlyConfigured
# exception if SECRET_KEY not in os.environ
try:
    SECRET_KEY = env("SECRET_KEY")
except ImproperlyConfigured:
    SECRET_KEY = os.environ.get("SECRET_KEY")


# APPS
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
THIRD_PARTY_APPS = [
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "crispy_forms",
    "crispy_bootstrap5",
    "djstripe",
    "django_htmx",
    "sorl.thumbnail",
    "markdownx",
]
LOCAL_APPS = [
    "users.apps.UsersConfig",
    "store.products",
    "store.cart",
    "store.orders",
    "store.checkout",
    "store.reviews",
    "store.wishlist",
    "classes",
    "blog",
    "contact",
    "admin_dashboard",
]

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

# allauth specific settings
AUTHENTICATION_BACKENDS = [
    # Needed for Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = 1

LOGIN_REDIRECT_URL = "products:store"
ACCOUNT_EMAIL_REQUIRED = True

# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         # For each OAuth based provider, either add a ``SocialApp``
#         # credentials, or list them here:
#         'APP': {
#             'client_id': '123',
#             'secret': '456',
#             'key': ''
#         }
#     }
# }

# crispy form specific settings
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # `allauth` needs this from django
                "django.template.context_processors.request",
            ],
        },
    },
]


# URLS
ROOT_URLCONF = "core.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "core.wsgi.application"


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# LOGGING
# See https://docs.djangoproject.com/en/dev/topics/logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": (
                "%(asctime)s [%(process)d] [%(levelname)s] "
                + "pathname=%(pathname)s lineno=%(lineno)s "
                + "funcname=%(funcName)s %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "null": {
            "level": "DEBUG",
            "class": "logging.NullHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "testlogger": {
            "handlers": ["console"],
            "level": "INFO",
        }
    },
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
    STRIPE_LIVE_SECRET_KEY = os.environ.get("STRIPE_LIVE_SECRET_KEY", "")
    STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY", "")
    STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY", "")
    DJSTRIPE_WEBHOOK_SECRET = os.environ.get("DJSTRIPE_WEBHOOK_SECRET", "wh_secret")
    STRIPE_LIVE_MODE = os.environ.get("STRIPE_LIVE_MODE", False)
    DJSTRIPE_FOREIGN_KEY_TO_FIELD = os.environ.get(
        "DJSTRIPE_FOREIGN_KEY_TO_FIELD", "id"
    )
    DJSTRIPE_USE_NATIVE_JSONFIELD = True

    print("Stripe keys not found using django-environ", excep)
