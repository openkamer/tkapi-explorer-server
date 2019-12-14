import json
import logging

from django.http import JsonResponse

from tkapi import TKApi
from tkapi.activiteit import Activiteit
from tkapi.activiteit import Reservering
from tkapi.activiteit import Zaal
from tkapi.activiteit import ActiviteitActor
from tkapi.agendapunt import Agendapunt
from tkapi.besluit import Besluit
from tkapi.commissie import Commissie
from tkapi.commissie import CommissieContactinformatie
from tkapi.commissie import CommissieZetel
from tkapi.commissie import CommissieZetelVastPersoon
from tkapi.commissie import CommissieZetelVervangerPersoon
from tkapi.commissie import CommissieZetelVastVacature
from tkapi.commissie import CommissieZetelVervangerVacature
from tkapi.document import Document
from tkapi.document import DocumentActor
from tkapi.document import DocumentVersie
from tkapi.dossier import Dossier
from tkapi.fractie import Fractie
from tkapi.fractie import FractieZetel
from tkapi.fractie import FractieZetelPersoon
from tkapi.fractie import FractieZetelVacature
from tkapi.fractie import FractieAanvullendGegeven
from tkapi.persoon import Persoon
from tkapi.persoon import PersoonReis
from tkapi.persoon import PersoonGeschenk
from tkapi.persoon import PersoonOnderwijs
from tkapi.persoon import PersoonNevenfunctie
from tkapi.persoon import PersoonNevenfunctieInkomsten
from tkapi.persoon import PersoonContactinformatie
from tkapi.stemming import Stemming
from tkapi.vergadering import Vergadering
from tkapi.verslag import Verslag
from tkapi.zaak import Zaak
from tkapi.zaak import ZaakActor
from tkapi.filter import VerwijderdFilter


logger = logging.getLogger(__name__)

api = TKApi(verbose=True)

entity_types = [
    Fractie,
    Zaal,
    ActiviteitActor,
    CommissieContactinformatie,
    CommissieZetel,
    CommissieZetelVastPersoon,
    CommissieZetelVervangerPersoon,
    CommissieZetelVastVacature,
    CommissieZetelVervangerVacature,
    DocumentActor,
    DocumentVersie,
    FractieZetel,
    FractieZetelPersoon,
    FractieZetelVacature,
    FractieAanvullendGegeven,
    PersoonOnderwijs,
    PersoonNevenfunctie,
    PersoonNevenfunctieInkomsten,
    PersoonContactinformatie,
    ZaakActor,
    Dossier,
    Persoon,
    Document,
    Zaak,
    Commissie,
    Stemming,
    Activiteit,
    Reservering,
    Agendapunt,
    Besluit,
    Verslag,
    Vergadering,
    PersoonReis,
    PersoonGeschenk,
]


def get_tkitem_class_for_type(type_str):
    for entity in entity_types:
        if entity.url == type_str:
            return entity
    return None


def get_entity_types(request):
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
    for entity_type in entity_types:
        # print(entity_type.type)
        # items = api.get_items(type, max_items=0)
        # items_json = [item.json for item in items]
        entities.append({
            'type': entity_type.type,
            'items': []
        })
    return JsonResponse(entities, safe=False)


def get_entity_links(request):
    logger.info('BEGIN')
    entity_url = request.GET.get('entity_url')
    related_type = request.GET.get('related_type')
    url = '{}/{}'.format(entity_url, related_type)
    # deleted_filter = VerwijderdFilter()
    # deleted_filter.filter_verwijderd()
    # params = {
    #     '$filter': deleted_filter.filter_str
    # }
    params = {}
    response = api._request_json(url=url, params=params)
    # print(response)
    links = []
    if 'value' in response:
        links = response['value']
    elif '@odata.type' in response:
        links.append(response)
    logger.info('END')
    return JsonResponse(links, safe=False)


def get_entities_by_url(request):
    logger.info('BEGIN')
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

    tkitem_class = get_tkitem_class_for_type(url)
    if tkitem_class is not None:
        params = api.create_query_params(tkitem_class)
    else:
        params = {}
        # if 'filter' not in url:
        #     deleted_filter = VerwijderdFilter()
        #     deleted_filter.filter_verwijderd()
        #     params = {
        #         '$filter': deleted_filter.filter_str
        #     }

    if skip_items is not None:
        params['$skip'] = skip_items
    if return_count:
        params['$count'] = 'true'
    logger.info('END')
    return get_entities(url, params=params, max_items=max_items, skip_items=skip_items, return_count=return_count)


def get_entities(url, params, max_items=None, skip_items=None, return_count=False):
    logger.info('BEGIN')
    print('get_entities', url, max_items, skip_items, return_count)
    response = api._request_json(url=url, params=params, max_items=max_items)
    # print('RESPONSE', json.dumps(response, indent=2))
    next_page_link = None
    items_json = response
    total_items = None
    if return_count and '@odata.count' in response:
        total_items = response['@odata.count']
    if 'value' in response:
        items_json = response['value']
    if '@odata.nextLink' in response:
        next_page_link = response['@odata.nextLink']
    entities = {
        'items': items_json,
        'total_items': total_items,
        'next_page_link': next_page_link
    }
    logger.info('END')
    return JsonResponse(entities, safe=False)
