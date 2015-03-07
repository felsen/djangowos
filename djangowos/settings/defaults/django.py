"""
Default Django settings
"""

import os
import os.path

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../..')

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'djangowos.frontend',
    'djangowos.package',

    'compressor',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'sass --scss --compass {infile} {outfile}'),
)

SITE_ROOT = os.path.join(BASE_DIR, 'site')
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

LOGGING = {
    'version': 1,
    'formatters': {
        'message_only': {
            'format': '%(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'message_only'
        }
    },
    'loggers': {
        'pypi_data': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}

ROOT_URLCONF = 'djangowos.urls'
WSGI_APPLICATION = 'djangowos.wsgi.application'

TIME_ZONE = 'UTC'
USE_TZ = True

LANGUAGE_CODE = 'en-us'
USE_I18N = False
USE_L10N = False

STATIC_URL = '/static/'
