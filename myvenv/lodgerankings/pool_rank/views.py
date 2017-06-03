from django.shortcuts import render, HttpResponseRedirect, reverse
from django.shortcuts import get_object_or_404

from house.models import Player
from .models import PoolScore, PoolGame

from forms import PoolGameForm

from rank_functions import update_players, get_recent_games

# Create your views here.


def index(request):
    return render(request, 'pool_rank/index.html', {})


def rankings(request):
    scores = PoolScore.objects.order_by('-score')
    percents = PoolScore.objects.order_by('-win_percent')
    highest_percent = percents[0]
    lowest_percent = percents[len(percents) - 1]
    wins = PoolScore.objects.order_by('-wins')
    most_wins = wins[0]
    losses = PoolScore.objects.order_by('-losses')
    most_losses = losses[0]
    games_played = PoolScore.objects.order_by('-games_played')
    most_games = games_played[0]
    fewest_games = games_played[len(games_played) - 1]

    return render(request, 'pool_rank/rankings.html',
        {'scores': scores,
            'highest_percent': highest_percent,
            'lowest_percent': lowest_percent,
            'most_wins': most_wins,
            'most_losses': most_losses,
            'most_games': most_games,
            'fewest_games': fewest_games})


def recent_games(request):
    games = PoolGame.objects.order_by('-date')
    games1 = games[:3]
    games2 = games[3:6]
    games3 = games[6:9]
    return render(request, 'pool_rank/recent_games.html',
        {'games1': games1,
            'games2': games2,
            'games3': games3})


def add_game(request):
    if request.method == 'POST':
        form = PoolGameForm(request.POST)
        if form.is_valid():
            winner1 = form.cleaned_data['winner1']
            winner2 = form.cleaned_data['winner2']
            loser1 = form.cleaned_data['loser1']
            loser2 = form.cleaned_data['loser2']
            date = form.cleaned_data['date']
            update_players(winner1, winner2, loser1, loser2, date)
            return HttpResponseRedirect(reverse('pool_rank:add_game'))
        else:
            msg = 'Error: invalid form'
            return render(request, 'pool_rank/add_game.html', {'msg': msg})
    else:
        form = PoolGameForm()

    return render(request, 'pool_rank/add_game.html', {'form': form})


def players(request):
    players = Player.objects.order_by('last_name')
    return render(request, 'pool_rank/players.html', {'players': players})


def player_detail(request, netid):
    scores = PoolScore.objects.order_by('-score')
    place = 1
    for score in scores:
        if score.player.netid == netid:
            break
        else:
            place += 1
    player = get_object_or_404(Player, pk=netid)
    recent_wins1 = PoolGame.objects.all().filter(winner1=netid)
    recent_wins2 = PoolGame.objects.all().filter(winner2=netid)
    recent_wins = get_recent_games(recent_wins1, recent_wins2, 3)
    recent_losses1 = PoolGame.objects.all().filter(loser1=netid)
    recent_losses2 = PoolGame.objects.all().filter(loser1=netid)
    recent_losses = get_recent_games(recent_losses1, recent_losses2, 3)
    score = get_object_or_404(PoolScore, player=player)
    return render(request, 'pool_rank/player_detail.html', {'player': player,
        'score': score, 'place': place, 'recent_wins': recent_wins,
        'recent_losses': recent_losses})
