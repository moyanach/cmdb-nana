from bson.objectid import ObjectId

from django.http.response import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder


class DjangoJSONEncoderExtra(DjangoJSONEncoder):
    """
    DjangoJSONEncoderExtra subclass that knows how to encode ObjectId.
    """

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        else:
            return super().default(o)


class JsonResponseExtra(JsonResponse):

    def __init__(self, data, encoder=DjangoJSONEncoderExtra, safe=True,
                 json_dumps_params=None, **kwargs):
        super().__init__(data=data, encoder=encoder, safe=safe, json_dumps_params=json_dumps_params, **kwargs)
