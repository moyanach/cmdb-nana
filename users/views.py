# Create your views here.
import json

from django.core.serializers.json import Serializer
from django.views.generic.list import BaseListView
from django.views.generic.base import View
from django.http.response import JsonResponse

from users.models import UsersModel


__all__ = ['UserListView', 'UsersLoginView']


class UserListView(BaseListView):

    model = UsersModel
    queryset = UsersModel.objects.all()

    def get_paginate_by(self, queryset):
        return self.request.GET.get('size', 10)

    def render_to_response(self, context):
        results = {'code': 200, 'msg': 'success', "data": [], 'total': 0}
        page = context.get('object_list', [])
        results['data'] = json.loads(Serializer().serialize(page))  # Serializer().serialize(page)
        results['total'] = self.get_queryset().count()
        return JsonResponse(data=results)


class UsersLoginView(View):

    def post(self, request):
        data = json.loads(request.body)
        results = {'code': 200, 'msg': 'success', "data": []}
        return JsonResponse(data=results)
