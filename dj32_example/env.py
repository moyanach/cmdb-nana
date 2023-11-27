
class TestEnv:

    MONGO_USER = "cmdb_rd"
    MONGO_PASSWORD = "CMdbsnt6N3line3r"
    MONGO_HOST = "10.89.108.21:27037,10.89.108.19:27037,10.89.120.21:27037"
    MONGO_DB = "ops_cmdb"
    REPLICASET = "device_v3"
    AUTH = 'admin'


class ProdEnv:

    MONGO_USER = "cmdb_rd"
    MONGO_PASSWORD = "CMdbsnt6N3line3r"
    MONGO_HOST = "10.89.108.21:27037,10.89.108.19:27037,10.89.120.21:27037"
    MONGO_DB = "ops_cmdb"
    REPLICASET = "device_v3"
    AUTH = 'admin'


test_config = TestEnv()
