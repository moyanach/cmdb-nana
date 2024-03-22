from pathlib import Path

from .config import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "73hy!ksrvt=0mp010hj*gvcu3#($s7ftqhov!+_eiz84thsnnl"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "channels",
    "project",
    "users",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "Kael.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "kaer.wsgi.application"
ASGI_APPLICATION = "kaer.asgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": config.MYSQL_HOST,
        "PORT": config.MYSQL_PORT,  # 监听端口
        "NAME": config.MYSQL_DB,  # 数据库名称【需要提前创建数据库】
        "USER": config.MYSQL_USER,  # 数据库用户名【默认是root】
        "PASSWORD": config.MYSQL_PWD,  # 上面数据库用户的密码
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # "LOCATION": f"redis://{config.SENTRY_HOST}/{config.REDIS_DB}",
        "LOCATION": [
            f"redis://{item.split(':')[0], item.split(':')[1]}"
            for item in config.SENTRY_HOST.split(",")
        ],
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.SentinelClient",
            "CONNECTION_FACTORY": "django_redis.pool.SentinelConnectionFactory",
            # "CONNECTION_POOL_CLASS": "redis.sentinel.SentinelConnectionPool",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 20,
                "decode_responses": True,
                "service_name": config.SERVICE_NAME,
            },
            "SENTINELS": [
                (item.split(":")[0], item.split(":")[1])
                for item in config.SENTRY_HOST.split(",")
            ],
            "SENTINEL_KWARGS": {"password": config.SENTRY_PASSWORD},
            "PASSWORD": config.REDIS_PASSWORD,
        },
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_L10N = True

USE_TZ = False


STATIC_URL = "/static/"
