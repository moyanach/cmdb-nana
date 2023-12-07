
from pathlib import Path

from .env import config
from common.mongo import mongo_connect_str

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '73hy!ksrvt=0mp010hj*gvcu3#($s7ftqhov!+_eiz84thsnnl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'application',
    'channels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dj32_example.urls'

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

WSGI_APPLICATION = 'dj32_example.wsgi.application'
ASGI_APPLICATION = 'dj32_example.asgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'ops_cmdb',
        'HOST': mongo_connect_str,
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # "LOCATION": f"redis://{config.SENTRY_HOST}/{config.REDIS_DB}",
        "LOCATION": [f"redis://{item.split(':')[0], item.split(':')[1]}" for item in config.SENTRY_HOST.split(',')],
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.SentinelClient",

            "CONNECTION_FACTORY": "django_redis.pool.SentinelConnectionFactory",
            # "CONNECTION_POOL_CLASS": "redis.sentinel.SentinelConnectionPool",
            "CONNECTION_POOL_KWARGS": {"max_connections": 20, "decode_responses": True, "service_name": config.SERVICE_NAME},

            "SENTINELS": [(item.split(':')[0], item.split(':')[1])for item in config.SENTRY_HOST.split(',')],
            "SENTINEL_KWARGS": {"password": config.SENTRY_PASSWORD},

            "PASSWORD": config.REDIS_PASSWORD,
        }
    }
}


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


LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


STATIC_URL = '/static/'
