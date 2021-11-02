from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path('info/lastupdate', views.last_update, name='last_update'),
    path('header/<str:profile_type>/<str:platform_number>/<str:cycle_number>', views.header, name='header'),
    path('profile/<str:profile_type>/<str:platform_number>/<str:cycle_number>', views.profile, name='profile_data'),
]