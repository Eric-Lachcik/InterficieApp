"""
Django settings for InterficieAppBack project.

Generated by 'django-admin startproject' using Django 5.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path
from decouple import config
import os

ENVIRONMENT = config('ENVIRONMENT', default='development')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-yy&w#0j0fzo_bdzxq2@t+-&r48srj#mlaqi3t2x!plni&rgg@k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'FitCoreBack',
    'rest_framework',
    'rest_framework_simplejwt',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'InterficieAppBack.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'InterficieAppBack.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'gymdb',
#         'USER': 'root',
#         'PASSWORD': 'root',
#         'HOST': 'localhost',
#         'PORT': '3307',
#         'OPTIONS': {
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES', default_storage_engine=INNODB",
#             'charset': 'utf8mb4',
#         },
#     }
# }

# Configuración de la base de datos
if ENVIRONMENT == 'production':
    DATABASES = {
        'default': {
            'ENGINE': config('DB_ENGINE'),
            'NAME': config('PROD_DB_NAME'),
            'USER': config('PROD_DB_USER'),
            'PASSWORD': config('PROD_DB_PASSWORD'),
            'HOST': config('PROD_DB_HOST'),
            'PORT': config('PROD_DB_PORT'),
        }
    }
else:  # development, testing, etc.
    DATABASES = {
        'default': {
            'ENGINE': config('DB_ENGINE'),
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT'),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SIMPLE_JWT = {
    'TOKEN_OBTAIN_SERIALIZER': 'FitCoreBack.serializers.SecureTokenObtainPairSerializer',
    'USER_ID_FIELD': 'id',
    'AUTH_HEADER_TYPES': ('JWT',),
}

INSTALLED_APPS += ['corsheaders']

MIDDLEWARE.insert(2, 'corsheaders.middleware.CorsMiddleware')

# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:8080",
#     "capacitor://localhost",
#     "http://192.168.1.100:8080",
#     "http://localhost:9000",
#     "http://127.0.0.1:9000",
# ]

# CORS_ALLOW_HEADERS = [
#     'accept',
#     'accept-encoding',
#     'authorization',
#     'content-type',
#     'dnt',
#     'origin',
#     'user-agent',
#     'x-csrftoken',
#     'x-requested-with',
#     'x-user-id',       # Añade estos dos encabezados personalizados
#     'x-user-role',
# ]

# CORS_EXPOSE_HEADERS = [
#     'x-user-id',
#     'x-user-role',
# ]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = '*' 
CORS_EXPOSE_HEADERS = '*'

CORS_ALLOW_CREDENTIALS = True

AUTH_USER_MODEL = 'FitCoreBack.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

MEDIA_URL = '/media/'  # URL para acceder a los archivos
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')  # Donde se guardarán los archivos
