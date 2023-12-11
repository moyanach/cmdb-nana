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
from project.models import BusinessesModel, ProductsModel, ApplicationModel  # noqa


class ProjectSyncData(SyncBaseInfo):

    APP_TYPE = {
        1: "phyiscs",
        2: "virtural",
    }

    APP_LANG = {
        1: "java",
        2: "go",
        3: "php",
        4: "python",
        5: "node",
    }

    is_docker = {
        0: 'common',
        1: 'docker',
    }

    # APP_COST_MODE = {
    #     "cpu": "计算型",
    #     "memory": "内存型",
    #     "disk": "磁盘型",
    # }

    APP_LEVEL = {
        1: "s",
        2: "a",
        3: "b",
    }

    def sync_business(self) -> list[dict]:
        api = '/api/cmdb/app/v2/business/'
        url = self.generate_url(api)
        total, pages = self.query_records_total(api)
        if not total:
            return []
        records = []
        print(pages)
        for page in pages:
            response = requests.get(url, headers=self.headers(), params={'page': page, 'size': self.page_size})
            try:
                print(response.url)
                results = response.json()
                print(results)
                records.extend(results.get('results', []))
            except Exception as err:
                print(err)
                pass
        print(records[0:1])
        print(len(records))
        return records

    def sync_product(self) -> list[dict]:
        api = '/api/cmdb/app/v2/product/'
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

    def sync_application(self) -> list[dict]:
        api = '/api/cmdb/app/v2/applications/'
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

    def save_businsess(self):
        reocrds = self.sync_business()
        for item in reocrds:
            item['instance'] = item['instance_id']
            item['description'] = item['description'] or ''
            del item['instance_id']
            del item['platform_label']
            user_obj = BusinessesModel(**item)
            try:
                user_obj.full_clean()
            except Exception as err:
                print(item)
        print('valid complate')
        for item in reocrds:
            user_obj = BusinessesModel(**item)
            user_obj.save()

    def save_product(self):
        objs = BusinessesModel.objects.only('instance', 'name')
        objs_map = {i.instance: i for i in objs}
        reocrds = self.sync_product()
        for item in reocrds:
            item['instance'] = item['instance_id']
            item['business'] = objs_map.get(item['business_id'])
            del item['instance_id']
            del item['code']
            del item['business_id']
            user_obj = ProductsModel(**item)
            try:
                user_obj.full_clean()
            except Exception as err:
                print(item)
        print('valid complate')
        for item in reocrds:
            try:
                print(item)
                user_obj = ProductsModel(**item)
                # user_obj.business = item['business']
                # user_obj.save()
                user_obj.save()
            except Exception as err:
                print(err)

    def save_application(self):
        objs = BusinessesModel.objects.only('instance', 'name')
        user_map = {i.instance: i for i in UsersModel.objects.only('instance')}
        product_map = {i.instance: i for i in ProductsModel.objects.only('instance')}
        objs_map = {i.instance: i for i in objs}
        reocrds = self.sync_application()
        app_rows = []
        for item in reocrds:
            item['instance'] = item['instance_id']
            item['business'] = objs_map.get(item['bussiness_id'])
            item['product'] = product_map.get(item['product_id'])
            item['owner'] = user_map.get(item['owner'])
            item['lang'] = self.APP_LANG.get(item['lang']) or 'java'
            item['level'] = self.APP_LEVEL.get(item['level'])
            item['mold'] = self.APP_TYPE.get(item['mold'])
            item['is_docker'] = self.is_docker.get(item['is_docker'])
            item['cost_mode'] = item['cost_mode'] or 'cpu'
            item['health'] = {'a': 'xx'}
            item['handle_info'] = 'xx'
            item['create_user'] = 'xx'
            item['description'] = item['description'] or 'xxx'
            # item['label'] = item['code']
            del item['instance_id']
            del item['product_id']
            del item['bussiness_id']
            del item['level_label']
            del item['cost_mode_label']
            del item['mold_label']
            del item['lang_label']
            del item['owner_user']
            user_obj = ApplicationModel(**item)
            try:
                user_obj.full_clean()
                app_rows.append(user_obj)
            except Exception as err:
                print(err, item)
                break
        print('valid complate')
        for row in app_rows:
            try:
                row.save()
            except Exception as err:
                print(err, row)
                break


if __name__ == '__main__':
    sync = ProjectSyncData()
    sync.save_application()
