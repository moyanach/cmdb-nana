
import os
from dotenv import load_dotenv


load_dotenv()


class TestEnv:

    MONGO_USER = os.getenv('MONGO_USER', '')
    MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', '')
    MONGO_HOST = os.getenv('MONGO_HOST', '')
    MONGO_DB = os.getenv('MONGO_DB', '')
    REPLICASET = os.getenv('REPLICASET', '')
    AUTH = os.getenv('AUTH', '')

    SENTRY_HOST = os.getenv('SENTRY_HOST', '')
    SENTRY_PASSWORD = os.getenv('SENTRY_PASSWORD', '')
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
    SERVICE_NAME = os.getenv('SERVICE_NAME', '')
    REDIS_DB = os.getenv('REDIS_DB', 0)


class ProdEnv:

    MONGO_USER = os.getenv('MONGO_USER', '')
    MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', '')
    MONGO_HOST = os.getenv('MONGO_HOST', '')
    MONGO_DB = os.getenv('MONGO_DB', '')
    REPLICASET = os.getenv('REPLICASET', '')
    AUTH = os.getenv('AUTH', '')

    SENTRY_HOST = os.getenv('SENTRY_HOST', '')
    SENTRY_PASSWORD = os.getenv('SENTRY_PASSWORD', '')
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
    SERVICE_NAME = os.getenv('SERVICE_NAME', '')
    REDIS_DB = os.getenv('REDIS_DB', 0)


config = TestEnv()
