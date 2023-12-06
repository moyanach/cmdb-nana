from pymongo.mongo_client import MongoClient

from dj32_example.env import config


def create_connect_client() -> MongoClient:
    conn_str = f"mongodb://{config.MONGO_USER}:{config.MONGO_PASSWORD}@{config.MONGO_HOST}/?authSource={config.AUTH}&replicaSet={config.REPLICASET}"
    client = MongoClient(conn_str)
    print('create mongo client')
    return client


mongo_client = create_connect_client()
