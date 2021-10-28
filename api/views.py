import json
import time

from django.http import HttpResponse
from django.http import JsonResponse

from django.db.models import Q

import api.models as models

import api.geojson as geojson


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

    print("Timing start")
    t1 = time.time_ns() / 1000
    collection = geojson.create_point_collection(features)
    print(time.time_ns() / 1000 - t1)

    return HttpResponse(collection, content_type='application/json')


def core(request, platform_number, cycle_number):
    data = models.ArgoCore.objects.filter(platform_number=platform_number, cycle_number=cycle_number).first()

    features = []
    features.append(
        geojson.create_point_feature(
            str(data['platform_number']) + '@' + str(data['cycle_number']),
            [data['longitude'], data['latitude']],
            {
                'cycle_number': data['cycle_number'],
                'pressure': data['pressure'],
                'cpressure': data['cpressure'],
                'qpressure': data['qpressure'],
                'temperature': data['temperature'],
                'ctemperature': data['ctemperature'],
                'qtemperature': data['qtemperature'],
                'salinity': data['salinity'],
                'csalinity': data['csalinity'],
                'qsalinity': data['qsalinity']
            }
        )
    )

    collection = geojson.create_point_collection(features)

    return HttpResponse(json.dumps(collection), content_type='application/json')
