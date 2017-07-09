from django.shortcuts import get_object_or_404
from house.models import Player
from pool_rank.models import PoolScore, PoolGame
from pong_rank.models import PongScore, PongGame
from xbox_rank.models import XboxScore, XboxGame

import trueskill
from trueskill.backends import cdf
import math


def get_recent_games(l1, l2, n):
    """Returns a list of the most recent games from the two lists
        PARAMETERS:
            l1      [list of ____Game]
                    the first list
            l2      [list of ____Game]
                    the second list
            n       [integer]
                    the remaining number of games to pull"""
    
    # base cases
    if n == 0:
        return []
    if len(l1) == 0:
        return l2[:n]
    if len(l2) == 0:
        return l1[0:n]
    
    # recursion
    if l1[0] <= l2[0]:
        foo = l1[0]
        remaining = get_recent_games(l1[1:], l2, n - 1)
        return [foo] + remaining
    if l1[0] > l2[0]:
        foo = l2[0]
        remaining = get_recent_games(l1, l2[1:], n - 1)
        return [foo] + remaining


def update_players(w1, w2, l1, l2, date, sport):
    """Function to update player scores based on a new game, and create
    a new game object representing the game.
    
        PARAMETERS:
            w1      [String]
                    netid of the first winner
            w2      [String or null] (optional)
                    netid or the second winner
            l1      [String]
                    netid of the first loser
            l2      [String or null] (optional)
                    netid of teh second loser
            date    [Date]
                    date the game was played on
            sport   [String]
                    which sport was played
    
    Throws a 404 Error if any of the players or scores are not found."""
    
    env = trueskill.TrueSkill()
    winners = {}
    winners_prob = []
    losers = {}
    losers_prob = []
    
    # get the first winner
    winner1 = get_object_or_404(Player, pk=w1)
    if sport == 'pool':
        winner1_score = get_object_or_404(PoolScore, player=winner1)
    elif sport == 'pong':
        winner1_score = get_object_or_404(PongScore, player=winner1)
    elif sport == 'xbox':
        winner1_score = get_object_or_404(XboxScore, player=winner1)
    else:
        return
    winner1_rating = env.create_rating(winner1_score.mu, winner1_score.sigma)
    winners['w1'] = winner1_rating
    winners_prob.append(winner1_score)
    
    # get the first loser
    loser1 = get_object_or_404(Player, pk=l1)
    if sport == 'pool':
        loser1_score = get_object_or_404(PoolScore, player=loser1)
    elif sport == 'pong':
        loser1_score = get_object_or_404(PongScore, player=loser1)
    elif sport == 'xbox':
        loser1_score = get_object_or_404(XboxScore, player=loser1)
    else:
        return
    loser1_rating = env.create_rating(loser1_score.mu, loser1_score.sigma)
    losers['l1'] = loser1_rating
    losers_prob.append(loser1_score)
    
    # get the second winner only if it exists
    if w2:
        winner2 = get_object_or_404(Player, pk=w2)
        if sport == 'pool':
            winner2_score = get_object_or_404(PoolScore, player=winner2)
        elif sport == 'pong':
            winner2_score = get_object_or_404(PongScore, player=winner2)
        elif sport == 'xbox':
            winner2_score = get_object_or_404(XboxScore, player=winner2)
        else:
            return
        winner2_rating = env.create_rating(winner2_score.mu,
            winner2_score.sigma)
        winners['w2'] = winner2_rating
        winners_prob.append(winner2_score)
    
    # get the second loser only if it exists
    if l2:
        loser2 = get_object_or_404(Player, pk=l2)
        if sport == 'pool':
            loser2_score = get_object_or_404(PoolScore, player=loser2)
        elif sport == 'pong':
            loser2_score = get_object_or_404(PongScore, player=loser2)
        elif sport == 'xbox':
            loser2_score = get_object_or_404(XboxScore, player=loser2)
        else:
            return
        loser2_rating = env.create_rating(loser2_score.mu, loser2_score.sigma)
        losers['l2'] = loser2_rating
        losers_prob.append(loser2_score)
    
    teams = [winners, losers]
    
    # calculate rankings
    quality = win_probability(winners_prob, losers_prob)
    [winners, losers] = env.rate(teams, ranks=[0, 1])
    
    for k, v in winners.items():
        if k == 'w1':
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
    
    if sport == 'pool':
        game = PoolGame()
    elif sport == 'pong':
        game = PongGame()
    elif sport == 'xbox':
        game = XboxGame()
    else:
        return
    game.winner1 = winner1
    game.loser1 = loser1
    
    if w2:
        game.winner2 = winner2
    if l2:
        game.loser2 = loser2
    game.date = date
    game.percent = quality * 100
    game.publish()


def win_probability(winners, losers):
    delta_mu = sum([x.mu for x in winners]) - sum([x.mu for x in losers])
    sum_sigma = sum([x.sigma ** 2 for x in winners]) + sum([x.sigma ** 2 for x in losers])
    player_count = len(winners) + len(losers)
    denominator = math.sqrt(player_count * (trueskill.BETA * trueskill.BETA) + sum_sigma)
    return cdf(delta_mu / denominator)