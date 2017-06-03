from django.shortcuts import get_object_or_404
from house.models import Player
from pool_rank.models import PoolScore, PoolGame

import trueskill


def update_players_pool(w1, w2, l1, l2, date):
    env = trueskill.TrueSkill()
    winners = {}
    losers = {}

    winner1 = get_object_or_404(Player, pk=w1)
    winner1_score = get_object_or_404(PoolScore, player=winner1)
    winner1_rating = env.create_rating(winner1_score.mu, winner1_score.sigma)
    winners['w1'] = winner1_rating

    loser1 = get_object_or_404(Player, pk=l1)
    loser1_score = get_object_or_404(PoolScore, player=loser1)
    loser1_rating = env.create_rating(loser1_score.mu, loser1_score.sigma)
    losers['l1'] = loser1_rating

    if w2:
        print 'adding second player'
        winner2 = get_object_or_404(Player, pk=w2)
        winner2_score = get_object_or_404(PoolScore, player=winner2)
        winner2_rating = env.create_rating(winner2_score.mu,
            winner2_score.sigma)
        winners['w2'] = winner2_rating
    if l2:
        loser2 = get_object_or_404(Player, pk=l2)
        loser2_score = get_object_or_404(PoolScore, player=loser2)
        loser2_rating = env.create_rating(loser2_score.mu, loser2_score.sigma)
        losers['l2'] = loser2_rating

    teams = [winners, losers]

    quality = env.quality(teams)
    [winners, losers] = env.rate(teams, ranks=[0, 1])

    for k, v in winners.items():
        print 'in winners'
        if k == 'w1':
            print 'where i should be'
            winner1_score.mu = v.mu
            winner1_score.sigma = v.sigma
            winner1_score.score = v.mu - 3 * v.sigma
            winner1_score.games_played += 1
            winner1_score.wins += 1
            winner1_score.win_percent = float(
                winner1_score.wins) / float(winner1_score.games_played) * 100.0
            winner1_score.publish()
        if k == 'w2':
            winner2_score.mu = v.mu
            winner2_score.sigma = v.sigma
            winner2_score.score = v.mu - 3 * v.sigma
            winner2_score.games_played += 1
            winner2_score.wins += 1
            winner2_score.win_percent = float(
                winner2_score.wins) / float(winner2_score.games_played) * 100.0
            winner2_score.publish()
    for k, v in losers.items():
        print 'in losers'
        if k == 'l1':
            loser1_score.mu = v.mu
            loser1_score.sigma = v.sigma
            loser1_score.score = v.mu - 3 * v.sigma
            loser1_score.games_played += 1
            loser1_score.losses += 1
            loser1_score.win_percent = float(
                loser1_score.wins) / float(loser1_score.games_played) * 100.0
            loser1_score.publish()
        if k == 'l2':
            loser2_score.mu = v.mu
            loser2_score.sigma = v.sigma
            loser2_score.score = v.mu - 3 * v.sigma
            loser2_score.games_played += 1
            loser2_score.losses += 1
            loser2_score.win_percent = float(
                loser2_score.wins) / float(loser2_score.games_played) * 100.0
            loser2_score.publish()

    game = PoolGame()
    game.winner1 = winner1
    game.loser1 = loser1
    if w2:
        game.winner2 = winner2
    if l2:
        game.loser2 = loser2
    game.date = date
    game.percent = quality * 100
    game.publish()