from django.conf.urls import url

from . import views

app_name = 'xbox_rank'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]