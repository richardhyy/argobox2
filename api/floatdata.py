# from django.shortcuts import render
# from django.shortcuts import reverse
# from django.shortcuts import redirect
#
# from django.views import generic
# from django.http import HttpResponse
# from django.http import JsonResponse
#
# from django.db import connection
#
# from django.conf import settings
#
# from .models import Header
#
#
# DataFields = {
#     'core': ('pressure', 'cpressqure', 'qpressure', 'temperature', 'ctemperature', 'qtemperature', 'salinity', 'csalinity', 'qsalinity'),
# }
#
#
# def execute_raw_sql(sql, params=None):
#     with connection.cursor() as cursor:
#         cursor.execute(sql, params)
#         return cursor
#
#
# class _DataTable:
#     def __init__(self, platform_number, fields):
#         fixed_columns = ('platformnumber', 'cyclenumber')
#         self._platform_number = platform_number
#         self._placeholders = ','.join(['%s'] * (len(fields) + len(fixed_columns)))
#         self._fields = ','.join(fixed_columns + fields)
#
#
#
# class FloatData:
#     def __init__(self, platform_number):
#         # self.header = Header.objects.filter(platform_number=platform_number).first()
#         # if self.header is None:
#         #     raise Exception('Header does not exist')
#         # else:
#         self.platform_number = platform_number
#         self.table_name = 'floatdata.t' + str(self.platform_number) + 'core'
#
#     def table_exists(self, table_name):
#         execute_raw_sql("""
#         SELECT EXISTS (
#             SELECT FROM pg_tables
#             WHERE  schemaname = 'floatdata'
#             AND    tablename  = %s
#         )""", table_name)
#
#     def create_table(self):
#         execute_raw_sql("CREATE TABLE %s () INHERITS (public.argocore)", [self.table_name])
#
#     def insert_or_update(self, cyclenumber, pressure, cpressqure, qpressure, temperature, ctemperature, qtemperature,
#                          salinity, csalinity, qsalinity):
#         with connection.cursor() as cursor:
#             sql = """INSERT (platformnumber, cyclenumber, pressure, cpressqure, qpressure, temperature, ctemperature, qtemperature, salinity, csalinity, qsalinity)
#                      INTO " + self.table_name + " VALUES (%s, %s, %s, %s, %f, %f, %f, %f, %f, %f, %f)"""
#             return cursor.execute(sql, (self.platform_number, cyclenumber, pressure, cpressqure, qpressure, temperature, ctemperature, qtemperature,
#                      salinity, csalinity, qsalinity))
#
# # CREATE TABLE floatdata.t1900978core () INHERITS (public.argocore);
