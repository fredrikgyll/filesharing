from django.urls import path, re_path

from sharing import views

app_name = 'sharing'
urlpatterns = [
    path('', views.index, name='index'),
    re_path(
        r'get/(?P<url_hash>[0-9A-Fa-f]{32})', views.get_by_hash, name='get_by_hash'
    ),
]
