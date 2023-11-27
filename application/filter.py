from typing import Optional

from pydantic import Field

from common.filters import Filters


class ApplicationFilter(Filters):

    name: Optional[str] = Field(description='名称', json_schema_extra={"mode": 'regex'}, default=None)
    owner: Optional[str] = Field(description='Owner', json_schema_extra={"mode": 'eq'}, default=None)
