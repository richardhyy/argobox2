from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import redirect

from django.views import generic
from django.http import HttpResponse
from django.http import JsonResponse

from django.core import serializers
from django.core.paginator import Paginator
from django.conf import settings

from django.db.models import Window, Max, F

from django.views.decorators.csrf import csrf_exempt, csrf_protect

from .forms import UploadFileForm
from .forms import ArgoSearchForm

from collections import OrderedDict
from os.path import isfile


def index(request):
    return render(request, 'interface/index.html', locals())
