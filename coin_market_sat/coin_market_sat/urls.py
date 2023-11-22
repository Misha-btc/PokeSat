from django.contrib import admin
from django.urls import include, path
from django.urls import path

urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        '',
        include('sat_list.urls', namespace='sat_list')
    )
]
