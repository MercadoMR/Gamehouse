import os
from django.urls import reverse_lazy
from decouple import config 


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

SECRET_KEY = config('SECRET_KEY')
#DEBUG = config('DEBUG', default=False, cast=bool)


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth', #Para autenticacion
    'django.contrib.contenttypes', #Para autenticacion
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #Sistema de jugadores 
    'gamehouse.sjug',
    #Sistema de administradores
    'gamehouse.sadm',
    'django_filters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', #Manage sessions across requests
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', #Associates users with requests using sessions
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gamehouse.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #directorio templates
        'DIRS': ['%s/templates/' %(BASE_DIR)],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'gamehouse.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#Checar https://stackoverflow.com/questions/4876370/django-date-format-dd-mm-yyyy 
DATE_INPUT_FORMATS = ('%d/%m/%Y','%d-%m-%Y') #('%d-%m-%Y','%Y-%m-%d')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_ROOT =  os.path.join(BASE_DIR, 'assets')
STATIC_URL = '/static/'
STATICFILES_DIRS = [STATIC_DIR,
  ('css','%s/css' % STATIC_DIR),
  ('js','%s/js' % STATIC_DIR),
 #('bootstrap','%s/bootstrap-3.1.1-dist/'% (STATIC_DIR)),
 #('jquery','%s/jquery-1-11-1-dist/'% (STATIC_DIR)),
 #('jquery-ui','%s/jquery-ui-1.10.4/'% (STATIC_DIR)), 
]

## Media: https://www.caktusgroup.com/blog/2017/08/28/advanced-django-file-handling/

MEDIA_ROOT = os.path.join(BASE_DIR, 'var/media')
MEDIA_URL = '/media/'

## Carpeta que tendra los vectores generados
ANALITYCS_DIR = os.path.join(BASE_DIR, 'var/analitycs/')
## Carpeta que tiene los algoritmos
ALGORITHMS_DIR = os.path.join(PROJECT_DIR, 'algorithms/')

""" Redireccionamiento automatico """
#https://docs.djangoproject.com/en/3.1/ref/settings/#login-url
LOGIN_REDIRECT_URL = reverse_lazy('dashboard')
LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/'

def crear_externos():
    """ Funcion para crear archivos TF-IDF si no existen """
    if not os.path.isfile(ALGORITHMS_DIR+'lemmas.pkl'):
        from gamehouse.algorithms.generation import generate_lemmas
        generate_lemmas(ALGORITHMS_DIR)
    if not os.path.isfile(ALGORITHMS_DIR+'tagger.pkl'):
        from gamehouse.algorithms.generation import generate_tagger
        generate_tagger(ALGORITHMS_DIR)
    return

crear_externos()

