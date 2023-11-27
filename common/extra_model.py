from typing import Optional, Dict, List, Tuple, Any

from pymongo.cursor import Cursor
from pymongo.results import UpdateResult, DeleteResult, InsertOneResult, InsertManyResult

from dj32_example.env import test_config as config
from common.mongo import mongo_client
from pydantic import BaseModel


class DataBaseExecExtra(BaseModel):

    def __init__(self, **data):
        super().__init__(**data)

    @classmethod
    def table_name(cls) -> str:
        return 'test_test'

    @classmethod
    def extra_return_fields(cls, excludes: Optional[list[str]] = None) -> dict[str, int]:
        base_fields = [item for item in cls.model_fields]
        fields = {i: 1 for i in base_fields}
        if excludes is not None:
            fields.update({i: 0 for i in excludes})
        return fields

    @classmethod
    def extra_create(cls, create_data: Dict) -> InsertOneResult:
        table_name = cls.table_name()
        documtent = mongo_client[config.MONGO_DB][table_name]
        record = documtent.insert_one(create_data)
        return record

    @classmethod
    def extra_batch_create(cls, create_data: List[Dict]) -> InsertManyResult:
        table_name = cls.table_name()
        documtent = mongo_client[config.MONGO_DB][table_name]
        record = documtent.insert_many(create_data)
        return record

    @classmethod
    def extra_delete(cls, data: dict) -> DeleteResult:
        table_name = cls.table_name()
        documtent = mongo_client[config.MONGO_DB][table_name]
        results = documtent.delete_many(data)
        return results

    @classmethod
    def extra_query_one(cls, find_kwargs: Dict, return_fields: dict) -> Optional[Any]:
        table_name = cls.table_name()
        documtent = mongo_client[config.MONGO_DB][table_name]
        item = documtent.find_one(find_kwargs, return_fields)
        return item

    @classmethod
    def extra_query_many(cls,
                         page: int,
                         size: int,
                         find_kwargs: Dict,
                         return_fields: Dict,
                         sort: Optional[List[Tuple[str, int]]] = None) -> Tuple[int, Cursor]:
        skip = (page - 1) * size
        table_name = cls.table_name()
        documtent = mongo_client[config.MONGO_DB][table_name]
        cursor = documtent.find(find_kwargs, return_fields).sort(sort).limit(size).skip(skip) \
            if sort else documtent.find(find_kwargs, return_fields).limit(size).skip(skip)
        count = documtent.count_documents(find_kwargs)
        return count, cursor

    @classmethod
    def extra_query_all(cls,
                        find_kwargs: Dict[str, Any] = {},
                        return_fields: Dict[str, Any] = {},
                        sort: Optional[List[Tuple[str, int]]] = None) -> Tuple[int, Cursor]:
        table_name = cls.table_name()
        documtent = mongo_client[config.MONGO_DB][table_name]
        cursor = documtent.find(find_kwargs, return_fields).sort(sort) if sort else documtent.find(find_kwargs, return_fields)
        count = documtent.count_documents(find_kwargs)
        return count, cursor

    @classmethod
    async def update_record_one(cls, update_info: Dict, find_kwargs: Dict = {}) -> UpdateResult:
        """
        根据 查询条件 更新单条记录 
        """
        table_name = cls.table_name()
        document = mongo_client[config.MONGO_DB][table_name]
        results = document.update_one(find_kwargs, {"$set": update_info})
        return results

    @classmethod
    async def update_record_many(cls, update_info: Dict, find_kwargs: Dict = {}) -> UpdateResult:
        """
        根据 查询条件 更新多条记录 
        """
        table_name = cls.table_name()
        document = mongo_client[config.MONGO_DB][table_name]
        results = document.update_many(find_kwargs, {"$set": update_info})
        return results
