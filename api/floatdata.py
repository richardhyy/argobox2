from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import redirect

from django.views import generic
from django.http import HttpResponse
from django.http import JsonResponse

from django.db import connection

from django.conf import settings


def execute_raw_sql(sql, params=None):
    with connection.cursor() as cursor:
        return cursor.execute(sql, params)


class ArgoCore:
    def __init__(self, platform_number):
        self.platform_number = platform_number

    def create_table(self):
        execute_raw_sql("CREATE TABLE floatdata.t" + str(self.platform_number) + "core () INHERITS (public.argocore)")

    def insert_or_update(self, cycle_number, pressure, cpressqure, qpressure, temperature, ctemperature, qtemperature,
                         salinity, csalinity, qsalinity):
        with connection.cursor() as cursor:
            sql = 'SELECT version()'
            cursor.execute(sql)
            row = cursor.fetchone()
            return HttpResponse(row)

# CREATE TABLE floatdata.t1900978core () INHERITS (public.argocore);
