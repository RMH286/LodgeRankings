from django.conf.urls import url

from . import views

app_name = 'pong_rank'
urlpatterns = [
    # main home page for pong rankings
    url(r'^$', views.index, name='index'),
    # page to display house-wide rankings
    url(r'^rankings$', views.rankings, name='rankings'),
    # page to display house-wide rankings
    url(r'^recent_games$', views.recent_games, name='recent_games'),
    #page to add a game and update players
    url(r'^add_game$', views.add_game, name='add_game'),
    #page to list all players in the house for further information
    url(r'^players$', views.players, name='players'),
    # page for player specific information
    url(r'^(?P<netid>[a-z0-9]+)$', views.player_detail, name='player_detail')
]