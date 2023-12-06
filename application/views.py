# Create your views here.
import json
from bson.objectid import ObjectId

from django.views.generic import View
from django.http.request import HttpRequest

from common.cache import cache
from common.jsonresponse import JsonResponseExtra
from application.filter import ApplicationFilter
from application.models import ApplicationModel, BusinessModel, ProductModel


__all__ = ['ApplicationBaseView', 'ApplicationSingleView']


class ApplicationBaseView(View):

    def get(self, request: HttpRequest) -> JsonResponseExtra:
        cache.set('dj-test', 1133, 30)
        results = {'code': 200, 'msg': 'success', 'count': 0, 'data': {}}
        query_params = request.GET.dict()
        page = int(query_params.pop('page', 1))  # type: ignore
        size = int(query_params.pop('size', 1))  # type: ignore
        filter_fields = ApplicationFilter(**query_params).generate_filter_info() or {}  # type: ignore
        return_fields = ApplicationModel.extra_return_fields()
        count, cursor = ApplicationModel.extra_query_many(page, size, filter_fields, return_fields)
        # cursor_user = cursor.clone()
        # business-label-map
        _, bu_cursor = BusinessModel.extra_query_all(return_fields={'instance_id': 1, 'label': 1})
        bu_name_map = {item['instance_id']: item['label'] for item in bu_cursor}
        # product-label-map
        _, product_cursor = ProductModel.extra_query_all(return_fields={'instance_id': 1, 'name': 1})
        product_name_map = {item['instance_id']: item['name'] for item in product_cursor}
        extra_context = {'product_name_map': product_name_map, 'bu_name_map': bu_name_map}
        data = ApplicationModel.extra_serializer_many(cursor=cursor, **extra_context)
        results['data'] = data
        results['count'] = count
        print(cache.get('dj-test'))
        return JsonResponseExtra(data=results)

    def post(self, request: HttpRequest) -> JsonResponseExtra:
        results = {'code': 200, 'msg': 'success', 'count': 0, 'data': {}}
        data: dict = json.loads(request.body)
        create_results = ApplicationModel.extra_create(ApplicationModel(**data).model_dump())
        results['data'] = {"_id": create_results.inserted_id}
        return JsonResponseExtra(data=results)


class ApplicationSingleView(View):

    def get(self, request: HttpRequest, _id: str) -> JsonResponseExtra:
        results = {'code': 200, 'msg': 'success', 'count': 0, 'data': {}}
        return_fields = ApplicationModel.extra_return_fields()
        filter_fields = {'_id': ObjectId(_id)}
        item = ApplicationModel.extra_query_one(filter_fields, return_fields)
        results['data'] = item
        return JsonResponseExtra(data=results)

    def delete(self, request: HttpRequest, _id: str) -> JsonResponseExtra:
        results = {'code': 200, 'msg': 'success', 'count': 0, 'data': {}}
        ApplicationModel.extra_delete({'_id': ObjectId(_id)})
        return JsonResponseExtra(data=results)


class BusinessBaseView(View):

    def get(self, request: HttpRequest) -> JsonResponseExtra:
        results = {'code': 200, 'msg': 'success', 'count': 0, 'data': {}}
        query_params = request.GET.dict()
        page = int(query_params.pop('page', 1))  # type: ignore
        size = int(query_params.pop('size', 1))  # type: ignore
        return_fields = BusinessModel.extra_return_fields()
        count, cursor = BusinessModel.extra_query_many(page, size, {}, return_fields)
        data = [item for item in cursor]
        results['data'] = data
        results['count'] = count
        return JsonResponseExtra(data=results)


class ProductBaseView(View):

    def get(self, request: HttpRequest) -> JsonResponseExtra:
        results = {'code': 200, 'msg': 'success', 'count': 0, 'data': {}}
        query_params = request.GET.dict()
        page = int(query_params.pop('page', 1))  # type: ignore
        size = int(query_params.pop('size', 1))  # type: ignore
        return_fields = ProductModel.extra_return_fields()
        count, cursor = ProductModel.extra_query_many(page, size, {}, return_fields)
        data = [item for item in cursor]
        results['data'] = data
        results['count'] = count
        return JsonResponseExtra(data=results)
