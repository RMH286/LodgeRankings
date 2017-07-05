from django.conf.urls import url

from . import views

app_name = 'pool_rank'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^rankings$', views.rankings, name='rankings'),
    url(r'^recent_games$', views.recent_games, name='recent_games'),
    url(r'^add_game$', views.add_game, name='add_game'),
    url(r'^players$', views.players, name='players'),
    url(r'^(?P<netid>[a-z0-9]+)$', views.player_detail, name='player_detail')
]