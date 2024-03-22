from typing import Any

import requests

from kaer.env import config


class SyncBaseInfo:

    def __init__(self) -> None:
        self.page_size = 100
        self.domain = config.CMDB_DOMAIN
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Inpob3VzaGlqaWUiLCJuaWNrbmFtZSI6Ilx1OWI1NFx1N2ZhZiIsIm5hbWUiOiJcdTU0NjhcdTRlMTZcdTY3NzAiLCJleHAiOjE4MjU3NDk4NDB9.FPLZK8nIIm8ZDD6ymubX4E-saDtNbWzu4TGRlkqaRfU'

    def headers(self) -> dict:
        return {"Authorization": f"Bearer {self.token}"}

    def generate_url(self, api_path: str) -> str:
        return f'{self.domain}{api_path}'

    def query_records_total(self, url: str) -> tuple[int, list[int]]:
        url = self.generate_url(url)
        response = requests.get(url, headers=self.headers())
        try:
            results = response.json()
            total = results.get('total', 0)
            # if total and total <= self.page_size:
            #     max_page = 1
            # else:
            max_page = int(total / self.page_size) + 1 if total % self.page_size > 0 else int(total / self.page_size)
            page_list = [i for i in range(1, max_page + 1)]
            return total, page_list
        except Exception as err:
            return 0, []
