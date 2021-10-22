from django.http import HttpResponse
from django.http import JsonResponse

from django.db.models import Q

import api.models as models


def header(request, platform_number, cycle_number):
    query = models.ArgoHeader.objects
    if platform_number != 'all':
        query = query.filter(platform_number=platform_number)
    if cycle_number == 'latest':
        query = query.order_by('platform_number', '-date').distinct('platform_number')
    elif cycle_number != 'all':
        query = query.filter(cycle_number=cycle_number)

    data_list = list(query.values())
    return JsonResponse(data_list, safe=False)


def core(request, platform_number, cycle_number):
    data = models.ArgoCore.objects.filter(platform_number=platform_number, cycle_number=cycle_number).first()
    return JsonResponse(data, safe=False)
