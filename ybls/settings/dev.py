from .base import *  # noqa

# whitenoise
# ------------------------------------------------------------------------------
INSTALLED_APPS.insert(0, 'whitenoise.runserver_nostatic')  # noqa F405
