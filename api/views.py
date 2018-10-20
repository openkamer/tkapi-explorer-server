from django.http import JsonResponse
from api.local_settings import TKAPI_USER, TKAPI_PASSWORD, TKAPI_ROOT_URL

from tkapi import Api
from tkapi.actor import FractieLid, Fractie, Persoon, Lid
from tkapi.activiteit import Activiteit
from tkapi.agendapunt import Agendapunt
from tkapi.besluit import Besluit
from tkapi.commissie import Commissie, VoortouwCommissie
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
    entities.append({
        'type': 'Verslag',
        'items': []
    })
    entities.append({
        'type': 'Vergadering',
        'items': []
    })
    return JsonResponse(entities, safe=False)


def get_entity_links(request):
    entity_url = request.GET.get('entity_url')
    related_type = request.GET.get('related_type')
    url = entity_url + '/$links/' + related_type
    deleted_filter = VerwijderdFilter()
    deleted_filter.filter_verwijderd()
    params = {
        '$filter': deleted_filter.filter_str
    }
    response = api.request_json(url=url, params=params)
    # print(response)
    links = []
    if 'value' in response:
        links = response['value']
    elif 'url' in response:
        links.append(response['url'])
    # print('LINKS', links)
    return JsonResponse(links, safe=False)


def get_entities_by_url(request):
    url = request.GET.get('url')
    max_items = request.GET.get('max_items', 10)
    skip_items = request.GET.get('skip_items', 0)
    is_single_item = request.GET.get('is_single_item', False)
    is_single_item = is_single_item == 'true'
    return_count = request.GET.get('return_count', False)
    if is_single_item:
        max_items = None
        skip_items = None
        return_count = False
    return get_entities(url, max_items, skip_items, return_count=return_count)


def get_entities(url, max_items=None, skip_items=None, return_count=False):
    print('get_entities', url, max_items, skip_items, return_count)
    params = None
    if 'filter' not in url:
        deleted_filter = VerwijderdFilter()
        deleted_filter.filter_verwijderd()
        params = {
            '$filter': deleted_filter.filter_str
        }
    if skip_items is not None:
        params['$skip'] = skip_items
    if return_count:
        params['$inlinecount'] = 'allpages'
    response = api.request_json(url=url, params=params, max_items=max_items)
    next_page_link = None
    items_json = response
    # print(items_json)
    total_items = None
    if return_count and 'odata.count' in response:
        total_items = response['odata.count']
    if 'value' in response:
        items_json = response['value']
    if 'odata.nextLink' in response:
        next_page_link = response['odata.nextLink']
    entities = {
        'items': items_json,
        'total_items': total_items,
        'next_page_link': next_page_link
    }
    return JsonResponse(entities, safe=False)


