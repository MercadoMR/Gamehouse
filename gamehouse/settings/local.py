from gamehouse.settings.base import *

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1','localhost']
ADMIN_ENABLED = True

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'gamehouse.db'),
    }
}

#Activar Admin

INSTALLED_APPS.append('django.contrib.admin')
## Correr en la consola para settings locales
#  export DJANGO_SETTINGS_MODULE=settings.local



