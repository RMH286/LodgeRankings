from django.shortcuts import render, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.http import Http404

from house.models import Player
from .models import PongScore, PongGame

from .forms import PongGameForm

from rank_functions import update_players, get_recent_games

# Create your views here.


def index(request):
    """Function to display the main homepage for the pool rankings.
    No extra work is required prior to rendering index.html."""
    
    return render(request, 'pong_rank/index.html', {})


def rankings(request):
    """Function to display the pool rankings page.
    This function must query the databse to retrieve the most current player
    score information. This includes all of the player scores as well as specific
    data; i.e. highest win percentage."""
    
    scores = PongScore.objects.order_by('-score')
    percents = PongScore.objects.order_by('-win_percent')
    if len(percents) > 0:
        highest_percent = percents[0]
        lowest_percent = percents[len(percents) - 1]
    else:
        highest_percent = "N/A"
        lowest_percent = "N/A"
    
    wins = PongScore.objects.order_by('-wins')
    losses = PongScore.objects.order_by('-losses')
    if len(wins) > 0:
        most_wins = wins[0]
        most_losses = losses[0]
    else:
        most_wins = "N/A"
        most_losses = "N/A"
    
    games_played = PongScore.objects.order_by('-games_played')
    if len(games_played) > 0:
        most_games = games_played[0]
        fewest_games = games_played[len(games_played) - 1]
    else:
        most_games = "N/A"
        fewest_games = "N/A"
    
    scores = PongScore.objects.order_by('-score')
    
    return render(request, 'pong_rank/rankings.html',
        {'scores': scores,
            'highest_percent': highest_percent,
            'lowest_percent': lowest_percent,
            'most_wins': most_wins,
            'most_losses': most_losses,
            'most_games': most_games,
            'fewest_games': fewest_games})


def recent_games(request):
    """Function to display the most recently played games in the house.
    The 9 most recent games are selected and split into three groups to be
    accessed in the html document."""
    
    games = PongGame.objects.order_by('-date')
    games1 = games[:3]
    games2 = games[3:6]
    games3 = games[6:9]
    
    return render(request, 'pong_rank/recent_games.html',
        {'games1': games1,
            'games2': games2,
            'games3': games3})


def add_game(request):
    """Function to display the form to add a game and update players.
    If a valid form has been submitted, this function must also handle the update
    of the player scores."""
    
    if request.method == 'POST':
        form = PongGameForm(request.POST)
        if form.is_valid():
            winner1 = form.cleaned_data['winner1']
            winner2 = form.cleaned_data['winner2']
            loser1 = form.cleaned_data['loser1']
            loser2 = form.cleaned_data['loser2']
            date = form.cleaned_data['date']
            try:
                update_players(winner1, winner2, loser1, loser2, date, 'pong')
            except Http404 as e:
                msg = 'Error: invalid netid'
                return render(request, 'pong_rank/add_game.html', {'form': form, 'msg': msg})
            return HttpResponseRedirect('pong_rank:add_game')
        else:
            msg = 'Error: invalid form'
            return render(request, 'pong_rank/add_game.html', {'form': form, 'msg': msg})
    else:
        form = PongGameForm()

    return render(request, 'pong_rank/add_game.html', {'form': form})


def players(request):
    """Function to display an index of all of the current players."""
    
    players = Player.objects.order_by('last_name')
    return render(request, 'pong_rank/players.html', {'players': players})


def player_detail(request, netid):
    """Function to display information on a single player. The player is
    specified by the netid which is part of the url. Various information must
    be queried from the database on the given player."""
    
    scores = PongScore.objects.order_by('-score')
    place = 1
    for score in scores:
        if score.player.netid == netid:
            break
        else:
            place += 1
    player = get_object_or_404(Player, pk=netid)
    # we require two queries in order to find the most recent wins since the
    # player could be winner1 or winner2
    # we then use the get_recent_games function to take the most recent 3 wins
    # from the two queries
    recent_wins1 = PongGame.objects.all().filter(winner1=netid).order_by(
        '-date')
    recent_wins2 = PongGame.objects.all().filter(winner2=netid).order_by(
        '-date')
    recent_wins = get_recent_games(recent_wins1, recent_wins2, 3)
    # we require two queries in order to find the most recent losses since the
    # player could be loser1 or loser2
    # we then use the get_recent_games function to take the most recent 3 losses
    # from the two queries
    recent_losses1 = PongGame.objects.all().filter(loser1=netid).order_by(
        '-date')
    recent_losses2 = PongGame.objects.all().filter(loser1=netid).order_by(
        '-date')
    recent_losses = get_recent_games(recent_losses1, recent_losses2, 3)
    score = get_object_or_404(PongScore, player=player)
     
    return render(request, 'pong_rank/player_detail.html', {'player': player,
        'score': score, 'place': place, 'recent_wins': recent_wins,
        'recent_losses': recent_losses})