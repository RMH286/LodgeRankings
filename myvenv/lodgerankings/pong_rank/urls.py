from django.conf.urls import url

from . import views

app_name = 'pong_rank'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]