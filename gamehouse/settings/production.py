from gamehouse.settings.base import *

DEBUG = False
ALLOWED_HOSTS = ['gamehome-escom.herokuapp.com']


#Configuracion de estaticos
MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware'] #Instalacion de Whitenoise en la aplicacion
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage" #Habilita compresion de archivos que servira

# Configuracion de la base de datos en Heroku
# Heroku: Update database configuration from $DATABASE_URL.
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES = { 
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2', 
		'NAME':'', 
		'USER':'', 
		'PASSWORD':'', 
		'HOST':'', 
		'PORT':'',
	}
}

DATABASES['default'].update(db_from_env)


"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': '',
    }
}
"""
## https://developer.mozilla.org/es/docs/Learn/Server-side/Django/Deployment
## Comandos para heroku, se ejecutan en la linea de comandos
## Poner nuestro Host:
## heroku config:set ALLOWED_HOSTS=<YOUR_UNIQUE_URL>
## Siguiente linea en heroku para escoger archivo settings correcto
## heroku config:set DJANGO_SETTINGS_MODULE=settings.production
## Para poner variable entorno secret key:
##heroku config:set SECRET_KEY='secret_key_goes_here'
## heroku config:set ADMIN_ENABLED=False
# Referencia : https://stackoverflow.com/questions/24071489/django-using-multiple-settings-files-with-heroku
# Refrencia: https://blog.heroku.com/from-project-to-productionized-python
# Referencia: https://blog.usejournal.com/deploying-django-to-heroku-connecting-heroku-postgres-fcc960d290d1
# Refrencia: https://developer.mozilla.org/es/docs/Learn/Server-side/Django/Deployment

#Popular DB en heroku con archivo sql:
#https://stackoverflow.com/questions/48180282/how-to-populate-a-heroku-postgresql-database-with-a-sql-file

#Desactivar Admin
#https://stackoverflow.com/questions/4845239/how-can-i-disable-djangos-admin-in-a-deployed-project-but-keep-it-for-local-de
