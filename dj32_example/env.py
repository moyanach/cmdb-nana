
import os
from dotenv import load_dotenv


load_dotenv()


class EnvConfig:

    """_summary_
       导入项目配置， 个别参数需要二次处理，请在此类中处理，保证项目内调用时可以直接使用
    """

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

    MYSQL_HOST = os.getenv('MYSQL_HOST', '')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_USER = os.getenv('MYSQL_USER', '')
    MYSQL_PWD = os.getenv('MYSQL_PWD', '')
    MYSQL_DB = os.getenv('MYSQL_DB', '')

    CMDB_DOMAIN = os.getenv('CMDB_DOMAIN', '')


config = EnvConfig()
