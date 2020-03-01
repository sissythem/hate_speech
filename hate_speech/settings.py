import json
import os
from os.path import join, exists
from os import getcwd, listdir, environ

import environ as envir


def load_properties():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    properties_file_path = join(dir_path, "properties.json") if exists(join(dir_path, "properties.json")) else \
        join(dir_path, "example_properties.json")
    with open(properties_file_path) as f:
        return json.loads(f.read())


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

all_properties = load_properties()
properties = all_properties["settings"]

SECRET_KEY = properties["SECRET_KEY"] if properties[
    "SECRET_KEY"] else '^7ql#lx3n&8=%u^139^fs*)=*x#ag)#9u+o(&v_&2*0--(zogg'

if properties["DATABASES"]:
    try:
        properties["DATABASES"]["HOST"] = environ["EXEC_REG_DB_SERVICE_HOST"]
        properties["DATABASES"]["PORT"] = environ["EXEC_REG_DB_SERVICE_PORT_MYSQL"]
    except (KeyError, Exception):
        pass

env = envir.Env(
    SECRET_KEY=str,
    DATABASE_ENGINE=(str, properties["DATABASES"]["ENGINE"]),
    DATABASE_NAME=(str, properties["DATABASES"]["NAME"]),
    DATABASE_USER=(str, properties["DATABASES"]["USER"]),
    DATABASE_PASS=(str, properties["DATABASES"]["PASSWORD"]),
    DATABASE_HOST=(str, properties["DATABASES"]["HOST"]),
    DATABASE_PORT=(str, properties["DATABASES"]["PORT"]),
    DEBUG=(bool, properties["DEBUG"]),
    ALLOWED_HOSTS=(list, properties["ALLOWED_HOSTS"]), )
envir.Env.read_env()

DATABASES = {
    'default': {
        'ENGINE': env('DATABASE_ENGINE'),
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASS'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT')
    }
}

DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'hate_speech_detection.apps.HateSpeechDetectionConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.RemoteUserBackend',
    'django.contrib.auth.backends.ModelBackend'
]


ROOT_URLCONF = 'hate_speech.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'hate_speech.wsgi.application'

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

STATIC_URL = '/static/'
STATIC_ROOT = join(BASE_DIR, "static")

TOKEN_TIMEOUT = 15  # timeout in minutes

SWAGGER_SETTINGS = {
    "exclude_namespaces": [],  # List URL namespaces to ignore
    "api_version": '0.1',  # Specify your API's version
    "api_path": "/",  # Specify the path to your API not a root level
    "enabled_methods": [  # Specify which methods to enable in Swagger UI
        'get',
        'post',
        'put',
        'delete'
    ],
    "is_authenticated": False,  # Set to True to enforce user authentication,
    "is_superuser": False,  # Set to True to enforce admin only access
    "permission_denied_handler": None,  # If user has no permisssion, raise 403 error
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'PAGINATE_BY': 20,
}

if not exists(join(BASE_DIR, "logs")):
    os.mkdir(join(BASE_DIR, "logs"))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': join(BASE_DIR, "logs", "logfile"),
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'exec_registry': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
    }
}
