from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from blog import views


urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        '',
        include('blog.urls', namespace='blog')
    ),
    path(
        'pages/',
        include('pages.urls', namespace='pages')
    ),
    path(
        'auth/',
        include('django.contrib.auth.urls')
    ),
    path(
        'auth/registration/',
        views.UserCreateView.as_view(),
        name='registration'
    )
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'
