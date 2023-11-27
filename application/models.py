# Create your models here.
from typing import Optional, Literal

from pydantic import Field
from pymongo.cursor import Cursor

from common.extra_model import DataBaseExecExtra
from application.enmu import AppLangEnmu, AppLevelEnmu, AppCostModeEnmu, AppTypeEnmu, DockerTypeEnmu


class ApplicationModel(DataBaseExecExtra):

    name: str = Field(max_length=64, description="应用名")
    owner: str = Field(max_length=32, description="应用owner")
    bussiness_id: str = Field(max_length=32, description="业务线ID")
    product_id: str = Field(max_length=32, description="产品线ID")
    lang: AppLangEnmu = Field(default=1, description="语言")
    level: AppLevelEnmu = Field(default=3, description="应用等级")
    mold: AppTypeEnmu = Field(default=1, description="应用类型")
    description: str = Field(default="", description="应用描述")
    cost_mode: AppCostModeEnmu = Field(default="cpu", description="容量模型")
    is_docker: DockerTypeEnmu = Field(default=0, description="容器应用")
    health: Optional[dict] = Field(default={}, description="服务健康度")
    handle_info: Optional[str] = Field(default='', description="服务健康度处理意见")

    @classmethod
    def table_name(cls) -> Literal['app_application']:
        return 'app_application'

    @classmethod
    def extra_serializer_many(cls, cursor: Cursor, *args, **kwargs) -> list[dict]:
        data = []
        bu_name_map = kwargs.get('bu_name_map', {})
        product_name_map = kwargs.get('product_name_map', {})
        for item in cursor:
            # 离谱, 原因：原始数据不规范，规范一次后，再实例化一次
            item_obj = cls(**cls(**item).model_dump())
            item['level_lable'] = item_obj.level.name
            item['lang_lable'] = item_obj.lang.name
            item['mold_lable'] = item_obj.mold.name
            item['cost_mode_lable'] = item_obj.cost_mode.name
            item['is_docker_lable'] = item_obj.is_docker.name
            item['bussiness_id_lable'] = bu_name_map.get(item_obj.bussiness_id, '')
            item['product_id_lable'] = product_name_map.get(item_obj.product_id, '')
            data.append(item)
        return data


class BusinessModel(DataBaseExecExtra):
    name: str = Field(max_length=32, description="业务线名称")
    label: str = Field(max_length=32, description="别名")
    platform: str = Field(max_length=32, description="所属平台")
    description: str = Field(max_length=32, description="描述信息")

    @classmethod
    def table_name(cls) -> Literal['app_business']:
        return 'app_business'


class ProductModel(DataBaseExecExtra):
    name: str = Field(max_length=32, description="业务线名称")
    code: str = Field(max_length=32, description="别名")
    description: str = Field(max_length=32, description="描述信息")
    business_id: str = Field(max_length=32, description="业务线ID")

    @classmethod
    def table_name(cls) -> Literal['app_product']:
        return 'app_product'


class ApplicationAsset(DataBaseExecExtra):
    name: str = Field(max_length=32, description="类型")
    parent_id: str = Field(max_length=32, description="应用ID")
    child_id: str = Field(max_length=32, default="0", description="资产ID")
    user: str = Field(max_length=32, default="0", description="用户ID")
    role: str = Field(max_length=32, default="0", description="角色")
    weight: str = Field(max_length=32, default="1", description="权重")

    @classmethod
    def table_name(cls) -> Literal['app_assets_relate']:
        return 'app_assets_relate'
