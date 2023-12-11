import os
import sys

import requests
import django

curPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(curPath)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj32_example.settings')
django.setup()

from utils.sync import SyncBaseInfo  # noqa
from users.models import UsersModel  # noqa


class SyncUserInfo(SyncBaseInfo):

    def __init__(self) -> None:
        super(SyncUserInfo, self).__init__()

    def sync_users(self) -> list[dict]:
        api = '/api/cmdb/user/v2/user/'
        url = self.generate_url(api)
        total, pages = self.query_records_total(api)
        if not total:
            return []
        records = []
        for page in pages:
            response = requests.get(url, headers=self.headers(), params={'page': page, 'size': self.page_size})
            try:
                results = response.json()
                records.extend(results.get('results', []))
            except Exception as err:
                pass
        print(records[0:1])
        print(len(records))
        return records

    def save_data(self):
        reocrds = self.sync_users()
        new_rows = []
        for item in reocrds:
            item['instance'] = item['instance_id']
            del item['instance_id']
            if 'organization_id' not in item:
                continue
            del item['organization_id']
            user_obj = UsersModel(**item)
            try:
                user_obj.full_clean()
                new_rows.append(user_obj)
            except Exception as err:
                print(item)
        print('valid complate')
        for row in new_rows:
            # del item['instance_id']
            # if 'organization_id' not in item:
            #     continue
            # del item['organization_id']
            # user_obj = UsersModel(**item)
            row.save()


if __name__ == '__main__':
    SyncUserInfo().save_data()
