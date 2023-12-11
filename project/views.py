# Create your views here.
import json

from django.views.generic.list import BaseListView
from django.views.generic.base import View
from django.utils.dateparse import parse_datetime
from django.http.response import JsonResponse
from django.core.serializers.json import Serializer

from project.models import ApplicationModel


__all__ = ('ProjectView', 'ProjectCreateView')


class ProjectView(BaseListView):

    model = ApplicationModel
    queryset = ApplicationModel.objects.all()

    def get_paginate_by(self, queryset):
        return self.request.GET.get('size', 10)

    def render_to_response(self, context):
        results = {'code': 200, 'msg': 'success', "data": []}
        page = context.get('object_list', [])
        data = Serializer().serialize(page).getvalue()
        results['data'] = data
        return JsonResponse(data=results)


class ProjectCreateView(View):

    def post(self, request):
        data = json.loads(request.body)
        results = {'code': 200, 'msg': 'success', "data": []}
        application_obj = ApplicationModel(**data)
        application_obj.full_clean()
        application_obj.save()
        return JsonResponse(data=results)
