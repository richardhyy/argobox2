from django.http import HttpResponse
from django.http import JsonResponse

from django.db.models import Q

from .models import Header
from api import floatdata


def header(request, platform_number, cycle_number):
    # WeatherReport.objects.order_by('city', '-date').distinct('city')

    data_list = list(Header.objects.filter(
        Q(platform_number=platform_number) & Q(cycle_number=cycle_number)
    ).values())

    # data_list = list(Header.objects.filter(
    #     Q(platform_number=platform_number) & Q(cycle_number=cycle_number)
    # ).values())
    return JsonResponse(data_list, safe=False)


def core(request, platform_number, cycle_number):
    # data_list = list(ArgoCore.objects.filter(
    #     Q(platform_number=platform_number) & Q(cycle_number=cycle_number)
    # ).values())
    argo_core = floatdata.ArgoCore(1900978)
    return JsonResponse(argo_core.platform_number, safe=False)
