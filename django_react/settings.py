import os
from datetime import timedelta
import dj_database_url
from multiprocessing import cpu_count

# SECURITY WARNING: don't run with debug turned on in production!
from celery.schedules import crontab

DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv('SECRET_KEY', 'sekrit')

CPU_SEPARATION = bool(int(os.getenv('CPU_SEPARATION', '1')))

ALLOWED_HOSTS = [os.getenv('APP_HOST'), '0.0.0.0', '127.0.0.1', 'localhost', '*']

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'spleeter-web.sqlite3',
    }
}

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

if 'TRAVIS' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'travisci',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

MEDIA_ROOT = 'media'
MEDIA_URL = '/media/'
SEPARATE_DIR = 'separate'
UPLOAD_DIR = 'uploads'

# Application definition
INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'allauth', 'allauth.account',
    'allauth.socialaccount',
    'rest_auth',
    'rest_auth.registration',
    'app.apps.AppConfig',
    'hm_site.apps.HmSiteConfig',
    'rest_framework',
    'knox',
    'corsheaders',
    'django_celery_beat',
    'django_celery_results',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_react.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'app', 'templates'),
                 os.path.join(BASE_DIR, 'hm_site', 'templates'), ],
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

WSGI_APPLICATION = 'django_react.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

SITE_ID = 1

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        'knox.auth.TokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
}

from rest_framework.settings import api_settings

REST_KNOX = {
    'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',
    'AUTH_TOKEN_CHARACTER_LENGTH': 64,
    'TOKEN_TTL': timedelta(days=7),
    'USER_SERIALIZER': 'api.serializers.CustomUserSerializer',
    'TOKEN_LIMIT_PER_USER': None,
    'AUTO_REFRESH': False,
    'EXPIRY_DATETIME_FORMAT': api_settings.DATETIME_FORMAT
}

TOKEN_DROPBOX = os.getenv('TOKEN_DROPBOX', 'M6iN1nYzh_YAAAAAAACUfhWR5kFUT-4Hwak6aAwSANv5vP0tLCHmnHCi37y9acqY')

SERVER_URL = os.environ.get('SERVER_URL', 'http://localhost:8000')

CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379')
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SELERLIZER = 'json'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

CELERY_TASK_ROUTES = {
    'app.tasks.fetch_youtube_audio': {
        'queue': 'fast_queue'
    },
    'app.tasks.fetch_upload_audio': {
        'queue': 'fast_queue'
    },
}

CORS_ALLOW_ALL_ORIGINS = True  # If this is used then `CORS_ALLOWED_ORIGINS` will not have any effect
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ORIGIN_WHITELIST = (
    'http://localhost:8000',
    'http://localhost:8080',
)

DATA_UPLOAD_MAX_NUMBER_FIELDS = None

VALID_MIME_TYPES = [
    'audio/aac', 'audio/aiff', 'audio/x-aiff', 'audio/ogg', 'video/ogg', 'application/ogg', 'audio/opus',
    'audio/vorbis', 'audio/mpeg',
    'audio/mp3', 'audio/mpeg3', 'audio/x-mpeg-3', 'video/mpeg', 'audio/m4a', 'audio/x-m4a', 'audio/x-hx-aac-adts',
    'audio/mp4', 'video/x-mpeg',
    'audio/flac', 'audio/x-flac', 'audio/wav', 'audio/x-wav', 'audio/webm', 'video/webm'
]

VALID_FILE_EXT = [
    # Lossless
    '.aif',
    '.aifc',
    '.aiff',
    '.flac',
    '.wav',
    # Lossy
    '.aac',
    '.m4a',
    '.mp3',
    '.opus',
    '.weba',
    '.webm',
    # Ogg (Lossy)
    '.ogg',
    '.oga',
    '.mogg'
]

UPLOAD_FILE_SIZE_LIMIT = 100 * 1024 * 1024
YOUTUBE_LENGTH_LIMIT = 30 * 60
YOUTUBE_MAX_RETRIES = 3

FILTERS_DEFAULT_LOOKUP_EXPR = 'icontains'

BROWSERSTACK_LOCAL_IDENTIFIER = os.getenv("BROWSERSTACK_LOCAL_IDENTIFIER")
BROWSERSTACK_USERNAME = os.getenv('BROWSERSTACK_USERNAME', 'caiodotdev_irwadE')
BROWSERSTACK_ACCESSKEY = os.getenv('BROWSERSTACK_ACCESSKEY', 'Ke15XkyiQ6qp9XryA26w')

LT_USERNAME = os.getenv('LT_USERNAME', 'caio.barbosa')
LT_ACCESS_KEY = os.getenv('LT_ACCESS_KEY', 'NaNNdBDJGhzbKMsigjJ2213wRT75vQDYqxtc9m7miNzzvMqV4P')
LT_ACCESS_TOKEN = os.getenv('LT_ACCESS_TOKEN', 'NaNNdBDJGhzbKMsigjJ2213wRT75vQDYqxtc9m7miNzzvMqV4P')
