from django.http import JsonResponse
from api.local_settings import TKAPI_USER, TKAPI_PASSWORD, TKAPI_ROOT_URL

from tkapi import Api
from tkapi.actor import FractieLid
from tkapi.actor import Fractie

api = Api(user=TKAPI_USER, password=TKAPI_PASSWORD)


def get_entities(request):
    lid_filter = FractieLid.create_filter()
    lid_filter.filter_actief()
    fractie_leden = api.get_fractie_leden(filter=lid_filter, max_items=5)
    fractie_leden = [lid.json for lid in fractie_leden]

    fractie_filter = Fractie.create_filter()
    fractie_filter.filter_actief()
    fracties = api.get_fracties(filter=fractie_filter, max_items=5)
    fracties = [fractie.json for fractie in fracties]

    entities = [
        {
            'name': FractieLid.url,
            'items': fractie_leden
        },
        {
            'name': Fractie.url,
            'items': fracties
        },
    ]
    return JsonResponse(entities, safe=False)


def get_entity(request):
    url = request.GET.get('url')
    response = api.request_json(url=url)
    if 'value' in response:
        response = response['value']
    entities = {
        'name': "unknown",
        'items': response
    }
    return JsonResponse(entities, safe=False)
