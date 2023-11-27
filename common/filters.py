import re
from typing import Optional, Literal, Any, Union

from pydantic import Field
from pydantic import BaseModel


class Filters(BaseModel):

    def __init__(self, **data):
        super().__init__(**data)

    def string_field_map(self, value: Any, mode: str) -> Union[Any, None]:
        map = {
            'regex': {'$regex': value},
            'like': re.compile(f'^{value}'),
            'eq': value,
        }
        return map.get(mode)

    def field_filter_expression(self, field_name: str, field_value: Any, filter_mode: str) -> Union[list[dict], None]:
        if isinstance(field_value, str):
            value = self.string_field_map(field_value, filter_mode) or field_value
            return [{field_name: value}]
        if isinstance(field_value, list) and filter_mode == 'in':
            return [{field_name: {'$in': field_value}}]
        if isinstance(field_value, list) and filter_mode == 'between':
            assert len(field_value) == 2
            return [{field_name: {"$gte": field_value[0]}}, {field_name: {"$lte": field_value[1]}}]
        return None

    def generate_filter_info(self, is_and: bool = True) -> Union[dict[str, list[Any]], None]:
        style = "$and" if is_and else "$or"
        search_kwargs = {style: []}
        data = self.model_dump(exclude_none=True)
        if not data:
            return None
        data_schema = self.model_json_schema().get('properties', {})
        for field, value in data.items():
            field_schema = data_schema.get(field)
            field_filter_mode = field_schema.get('mode', 'eq')
            expression = self.field_filter_expression(field, value, field_filter_mode)
            if expression is None:
                continue
            search_kwargs[style].extend(expression)
        return search_kwargs
