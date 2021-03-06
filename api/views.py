import json
import time

from django.http import HttpResponse
from django.http import JsonResponse

from django.db.models import Q
from django.forms.models import model_to_dict

from decimal import Decimal

import api.models as models

import api.geojson as geojson


ProfileTypeDict = {
    'core': models.ArgoCore.objects,
    'bbp': models.ArgoBbp.objects,
    'cdom': models.ArgoCdom.objects,
    'chla': models.ArgoChla.objects,
    'doxy': models.ArgoDoxy.objects,
    'irra': models.ArgoIrra.objects,
    'nitr': models.ArgoNitr.objects,
    'ph': models.ArgoPh.objects,
}


ProfileEssentialFields = ['platform_number', 'cycle_number']


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


def header(request, profile_type, platform_number, cycle_number):
    query = models.ArgoHeader.objects

    if profile_type != 'all':
        specified_type_platform_numbers = ProfileTypeDict[profile_type].all().values_list("platform_number")
        query = query.filter(platform_number__in=specified_type_platform_numbers)
    if platform_number != 'all':
        query = query.filter(platform_number=int(platform_number))
    if cycle_number == 'latest':
        query = query.order_by('platform_number', '-date').distinct('platform_number')
    elif cycle_number != 'all':
        query = query.filter(cycle_number=int(cycle_number))

    data_values = query.values()

    features = []
    for data in data_values:
        features.append(
            geojson.create_point_feature(
                str(data['platform_number']) + '@' + str(data['cycle_number']),
                [[data['longitude'], data['latitude']]],
                {
                    'platform_number': data['platform_number'],
                    'cycle_number': data['cycle_number'],
                    'date_creation': str(data['date_creation']),
                    'project_name': data['project_name'].replace('\'', ''),
                    'pi_name': data['pi_name'].replace('\'', ''),
                    'instrument_type': data['instrument_type'],
                    'sample_direction': data['sample_direction'],
                    'data_mode': data['data_mode'],
                    'julian_day': data['julian_day'],
                    'date': str(data['date'])
                }
            )
        )

    collection = geojson.create_point_collection(features)

    return HttpResponse(collection, content_type='application/json')


def profile(request, profile_type, platform_number, cycle_number):
    profile_model = ProfileTypeDict.get(profile_type)
    if profile_model is None:
        return HttpResponse("No such type")

    data = profile_model.filter(platform_number=platform_number, cycle_number=cycle_number).first()
    features = []

    if data is not None:
        data_dict = model_to_dict(data)
        # for k, v in model_to_dict(data):
        #     if k not in ProfileEssentialFields:
        #         data_dict[k] = v
        features.append(geojson.create_point_feature(
            'profile_' + str(data_dict['platform_number']) + '@' + str(data_dict['cycle_number']),
            None,
            json.dumps(data_dict, cls=DecimalEncoder)
        ))

    collection = geojson.create_point_collection(features)

    return HttpResponse(collection, content_type='application/json')


def last_update(request):
    response = {}
    last_date = None
    for profile_type in ProfileTypeDict.keys():
        _date = models.DatasetHistory.objects.filter(dataset_type=profile_type).order_by('-last_update').first().last_update
        if last_date is None:
            last_date = _date
        elif last_date < _date:
            last_date = _date
        response[profile_type] = _date
    response["overall_last"] = last_date
    return JsonResponse(response)
