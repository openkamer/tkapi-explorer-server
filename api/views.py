from django.http import JsonResponse
from api.local_settings import TKAPI_USER, TKAPI_PASSWORD, TKAPI_ROOT_URL

from tkapi import Api
from tkapi.actor import FractieLid, Fractie, Persoon, Lid
from tkapi.activiteit import Activiteit
from tkapi.agendapunt import Agendapunt
from tkapi.besluit import Besluit
from tkapi.commissie import Commissie, CommissieLid, VoortouwCommissie
from tkapi.document import ParlementairDocument
from tkapi.dossier import Dossier
from tkapi.stemming import Stemming
from tkapi.zaak import Zaak
from tkapi import VerwijderdFilter

api = Api(user=TKAPI_USER, password=TKAPI_PASSWORD, verbose=True)


def get_entity_types(request):
    entity_types = [
        Fractie,
        FractieLid,
        Dossier,
        Persoon,
        ParlementairDocument,
        Zaak,
        Commissie,
        Stemming,
        Activiteit,
        Agendapunt,
        Besluit,
    ]
    # lid_filter = FractieLid.create_filter()
    # lid_filter.filter_actief()
    # fractie_leden = api.get_fractie_leden(filter=lid_filter, max_items=5)
    # fractie_leden = [lid.json for lid in fractie_leden]
    #
    # fractie_filter = Fractie.create_filter()
    # fractie_filter.filter_actief()
    # fracties = api.get_fracties(filter=fractie_filter, max_items=5)
    # fracties = [fractie.json for fractie in fracties]

    entities = []
    for type in entity_types:
        print(type.url)
        # items = api.get_items(type, max_items=0)
        # items_json = [item.json for item in items]
        entities.append({
            'type': type.url,
            'items': []
        })
    return JsonResponse(entities, safe=False)


def get_entities_by_type(request, type):
    print('get_entities_by_type', type)
    deleted_filter = VerwijderdFilter()
    deleted_filter.filter_verwijderd()
    params = {
        '$filter': deleted_filter.filter_str
    }
    url = type
    print(url)
    response = api.request_json(url=url, params=params)
    if 'value' in response:
        response = response['value']
    entities = {
        'name': "unknown",
        'items': response
    }
    return JsonResponse(entities, safe=False)


def get_entities_by_url(request):
    url = request.GET.get('url')
    deleted_filter = VerwijderdFilter()
    deleted_filter.filter_verwijderd()
    params = {
        '$filter': deleted_filter.filter_str
    }
    response = api.request_json(url=url, params=params)
    if 'value' in response:
        response = response['value']
    entities = {
        'name': "unknown",
        'items': response
    }
    return JsonResponse(entities, safe=False)
