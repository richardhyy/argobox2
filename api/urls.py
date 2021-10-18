from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path('header/<str:platform_number>/<str:cycle_number>', views.header, name='header'),
    path('profile/core/<str:platform_number>/<str:cycle_number>', views.core, name='profile_core'),
]