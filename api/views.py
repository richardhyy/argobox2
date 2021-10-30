import json
import time

from django.http import HttpResponse
from django.http import JsonResponse

from django.db.models import Q

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


def header(request, platform_number, cycle_number):
    query = models.ArgoHeader.objects
    if platform_number != 'all':
        query = query.filter(platform_number=int(platform_number))
    if cycle_number == 'latest':
        query = query.order_by('platform_number', '-date').distinct('platform_number')
    elif cycle_number != 'all':
        query = query.filter(cycle_number=int(cycle_number))

    data_values = query.values()

    # TODO: Optimization - speed up model to json

    features = []
    for data in data_values:
        features.append(
            geojson.create_point_feature(
                str(data['platform_number']) + '@' + str(data['cycle_number']),
                [[data['longitude'], data['latitude']]],
                {
                    'cycle_number': data['cycle_number'],
                    'date_creation': str(data['date_creation']),
                    'project_name': data['project_name'],
                    'pi_name': data['pi_name'],
                    'instrument_type': data['instrument_type'],
                    'sample_direction': data['sample_direction'],
                    'data_mode': data['data_mode'],
                    'julian_day': data['julian_day'],
                    'date': str(data['date'])
                }
            )
        )

    # print("Timing start")
    t1 = time.time_ns() / 1000
    collection = geojson.create_point_collection(features)
    # print(time.time_ns() / 1000 - t1)

    return HttpResponse(collection, content_type='application/json')


def core(request, type, platform_number, cycle_number):
    profile_objects = ProfileTypeDict.get(type)
    if profile_objects is None:
        return HttpResponse("No such type")

    data = profile_objects.filter(platform_number=platform_number, cycle_number=cycle_number).first()
    features = []

    if data is not None:
        data_dict = {}
        for key, value in data:
            if key not in ProfileEssentialFields:
                data_dict[key] = value
        features.append(geojson.create_point_feature(
            str(data['platform_number']) + '@' + str(data['cycle_number']),
            None,
            data_dict
        ))

    collection = geojson.create_point_collection(features)

    return HttpResponse(collection, content_type='application/json')
