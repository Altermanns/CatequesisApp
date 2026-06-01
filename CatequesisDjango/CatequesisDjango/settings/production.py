import os
from .base import *

DEBUG = False
ALLOWED_HOSTS = ['*']  # Configurar para producción real

# Database configuration - SQLite (persistent in Render Disk)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db_data', 'db.sqlite3'),
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
