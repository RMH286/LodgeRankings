from django.shortcuts import render, HttpResponseRedirect, reverse

from house.models import Player
from .models import PoolScore, PoolGame

from forms import PoolGameForm

from rank_functions import update_players_pool

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
            update_players_pool(winner1, winner2, loser1, loser2, date)
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
    pass
"""
def recent_games(request):
    games = Game.objects.order_by('played_date')
    return render(request, 'ping_pong_rank/recent_games.html', {'games': games})


def add_game(request):
    return render(request, 'ping_pong_rank/add_game.html', {})


def update(request):
    if request.method == 'POST':
        try:
            entered_winner = request.POST['Winner_netid']
            entered_loser = request.POST['Loser_netid']
            entered_date = request.POST['Date_Played']
        except:
            return render(request, 'ping_pong_rank/add_game.html',
                {'error_message': "One or more fields were not entered"})
        try:
            game_winner = get_object_or_404(Player, pk=entered_winner)
            game_loser = get_object_or_404(Player, pk=entered_loser)
        except:
            return render(request, 'ping_pong_rank/add_game.html',
                {'error_message': "Invalid netid"})
        date = str(entered_date)
        game_winner.wins += 1
        game_loser.losses += 1
        game_winner.publish()
        game_loser.publish()
        index1 = date.find('-')
        index2 = date.rfind('-')
        year = int(date[:index1])
        month = int(date[index1 + 1:index2])
        day = int(date[index2 + 1:])
        date_object = datetime.date(year, month, day)
        game = Game(winner=str(game_winner.netid),
            loser=str(game_loser.netid),
            played_date=date_object)
        game.publish()
        return HttpResponseRedirect(reverse('ping_pong_rank:update'))
    elif request.method == 'GET':
        return render(request, 'ping_pong_rank/add_game.html', {})


def player_detail(request, netid):
    players = Player.objects.order_by('-score')
    place = 1
    for player in players:
        if player.netid == netid:
            break
        else:
            place += 1
    player = get_object_or_404(Player, pk=netid)
    recent_wins = Game.objects.all().filter(winner=netid).order_by('date')[:5]
    recent_losses = Game.objects.all().filter(loser=netid).order_by('date')[:5]
    d = {'player': player, 'place': place, 'recent_wins': recent_wins,
        'recent_losses': recent_losses}
    return render(request, 'ping_pong_rank/player_detail.html', d)
"""