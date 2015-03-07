"""
Development settings
"""

import os.path

from djangowos.settings.defaults import *

DEBUG = True
TEMPLATE_DEBUG = True

SECRET_KEY = 'local'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
