from django.urls import path

from . import views

app_name = 'sat_list'

urlpatterns = [
    path(
        '',
        views.SatListView.as_view(),
        name='index'
    ),
    # Другие URL-адреса вашего приложения...
]