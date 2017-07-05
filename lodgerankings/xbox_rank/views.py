from django.shortcuts import render, HttpResponseRedirect, reverse
from django.shortcuts import get_object_or_404

from house.models import Player
from .models import XboxScore, XboxGame

from forms import XboxGameForm

from rank_functions import update_players, get_recent_games

# Create your views here.


def index(request):
    return render(request, 'xbox_rank/index.html', {})


def rankings(request):
    scores = XboxScore.objects.order_by('-score')
    percents = XboxScore.objects.order_by('-win_percent')
    if len(percents) > 0:
        highest_percent = percents[0]
        lowest_percent = percents[len(percents) - 1]
    else:
        highest_percent = "N/A"
        lowest_percent = "N/A"
    wins = XboxScore.objects.order_by('-wins')
    losses = XboxScore.objects.order_by('-losses')
    if len(wins) > 0:
        most_wins = wins[0]
        most_losses = losses[0]
    else:
        most_wins = "N/A"
        most_losses = "N/A"
    games_played = XboxScore.objects.order_by('-games_played')
    if len(games_played) > 0:
        most_games = games_played[0]
        fewest_games = games_played[len(games_played) - 1]
    else:
        most_games = "N/A"
        fewest_games = "N/A"

    return render(request, 'xbox_rank/rankings.html',
        {'scores': scores,
            'highest_percent': highest_percent,
            'lowest_percent': lowest_percent,
            'most_wins': most_wins,
            'most_losses': most_losses,
            'most_games': most_games,
            'fewest_games': fewest_games})


def recent_games(request):
    games = XboxGame.objects.order_by('-date')
    games1 = games[:3]
    games2 = games[3:6]
    games3 = games[6:9]
    return render(request, 'xbox_rank/recent_games.html',
        {'games1': games1,
            'games2': games2,
            'games3': games3})


def add_game(request):
    if request.method == 'POST':
        form = XboxGameForm(request.POST)
        if form.is_valid():
            winner1 = form.cleaned_data['winner1']
            winner2 = form.cleaned_data['winner2']
            loser1 = form.cleaned_data['loser1']
            loser2 = form.cleaned_data['loser2']
            date = form.cleaned_data['date']
            update_players(winner1, winner2, loser1, loser2, date, 'xbox')
            return HttpResponseRedirect(reverse('xbox_rank:add_game'))
        else:
            msg = 'Error: invalid form'
            return render(request, 'xbox_rank/add_game.html', {'msg': msg})
    else:
        form = XboxGameForm()

    return render(request, 'xbox_rank/add_game.html', {'form': form})


def players(request):
    players = Player.objects.order_by('last_name')
    return render(request, 'xbox_rank/players.html', {'players': players})


def player_detail(request, netid):
    scores = XboxScore.objects.order_by('-score')
    place = 1
    for score in scores:
        if score.player.netid == netid:
            break
        else:
            place += 1
    player = get_object_or_404(Player, pk=netid)
    recent_wins1 = XboxGame.objects.all().filter(winner1=netid).order_by(
        '-date')
    recent_wins2 = XboxGame.objects.all().filter(winner2=netid).order_by(
        '-date')
    recent_wins = get_recent_games(recent_wins1, recent_wins2, 3)
    recent_losses1 = XboxGame.objects.all().filter(loser1=netid).order_by(
        '-date')
    recent_losses2 = XboxGame.objects.all().filter(loser1=netid).order_by(
        '-date')
    recent_losses = get_recent_games(recent_losses1, recent_losses2, 3)
    score = get_object_or_404(XboxScore, player=player)
    return render(request, 'xbox_rank/player_detail.html', {'player': player,
        'score': score, 'place': place, 'recent_wins': recent_wins,
        'recent_losses': recent_losses})