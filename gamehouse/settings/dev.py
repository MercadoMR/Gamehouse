from gamehouse.settings.base import *

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1','localhost']
ADMIN_ENABLED = True

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':os.environ.get('DB_NAME','gamehouse'),
	'USER':os.environ.get('DB_USER','postgres'),
	'PASSWORD':os.environ.get('DB_PASS','root'),
	'HOST':'localhost',
	'PORT':'5432',	
    }
}

#Activar Admin

INSTALLED_APPS.append('django.contrib.admin')
## Correr en la consola para settings locales
#  export DJANGO_SETTINGS_MODULE=settings.local

######1 cambiar databases por postgress
######2 hacer el dump de los datos sqlite
######3 Correr el sistema con postgress
######4 insertar datos del dump al postgress
######5 sbir a heroku
######6 checar pasos y subir el dump
######7 

#sudo -i -u postgres
#psql
#pip install psycopg2==2.7.5
#ALTER ROLE GAME SET client_encoding TO 'utf8';
#ALTER ROLE GAME SET default_transaction_isolation TO 'read committed';
#ALTER ROLE GAME SET timezone TO 'UTC';
#GRANT ALL PRIVILEGES ON DATABASE gamehouse TO GAME;

