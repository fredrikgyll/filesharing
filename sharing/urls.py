from django.urls import path

from sharing import views

app_name = 'sharing'
urlpatterns = [
    path('', views.index, name='index'),
]
