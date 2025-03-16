import environ
from pathlib import Path
from datetime import timedelta
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Initialize environ
env = environ.Env()

environ.Env.read_env(os.path.join(BASE_DIR, '../.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_^8n)h6-f+p=n6*b4zbc6&pdyh$_@b3^m5ihj7hv*y&lf*9!fg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    
    'django_filters',
    
    'rest_framework',
     'rest_framework_simplejwt',
     
     'channels',
     
     
    'accounts',
    'task'
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

ROOT_URLCONF = 'taskManagement.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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




# PostgreSQL settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'taskmanagementdb',
        'USER': 'admin',
        'PASSWORD': '123',
        'HOST': 'db',  # Use the service name from docker-compose.yml
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# DRF Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # Use JWT for authentication
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Protect endpoints that require authentication
    ],
}



# JWT Authentication settings (Optional: Customize JWT settings)
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # Access token will expire in 15 minutes
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),  # Refresh token will expire in 1 day
    'ROTATE_REFRESH_TOKENS': False,  # Do not rotate refresh tokens after use
    'BLACKLIST_AFTER_ROTATION': False,  # Do not blacklist refresh tokens after rotation
    'ALGORITHM': 'HS256',  # Algorithm to use for encoding JWT tokens
    'SIGNING_KEY': SECRET_KEY,  # Use your Django SECRET_KEY for signing JWT tokens
    'VERIFYING_KEY': None,  # None by default
    'AUTH_HEADER_TYPES': ('Bearer',),  # Expected authentication header prefix
    'USER_ID_FIELD': 'id',  # ID field for identifying the user in the JWT token
    'USER_ID_CLAIM': 'user_id',  # Claim name for user ID in the token payload
}

# Default Django settings for user authentication
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default authentication backend
]

WSGI_APPLICATION = 'taskManagement.wsgi.application'
#  for asgin calling and websockets
ASGI_APPLICATION = 'taskManagement.asgi.application'





# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)

EMAIL_HOST_USER = env('EMAIL_ID')

EMAIL_HOST_PASSWORD =env('EMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_USE_TLS = True




# Update cache settings to use Redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',  # Redis service name in Docker
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}




# Redis settings for Channels
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('redis', 6379)],  # Docker service name for Redis 0 db
        },
    },
}


CELERY_BROKER_URL = 'redis://redis:6379/3'  # Redis as the broker
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'redis://redis:6379/3'  # Redis as result backend
CELERY_TIMEZONE = 'UTC'


# Celery Beat Configuration (For periodic tasks)
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'send_notifications_at_10_am': {
        'task': 'task.tasks.send_due_task_notifications',
        'schedule': crontab(hour=10, minute=0),  # Trigger every day at 10:00 AM
    },
}




