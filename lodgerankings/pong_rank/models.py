from __future__ import unicode_literals

from django.db import models

# Create your models here.

MU = 25.0
SIGMA = 25.0 / 3.0


class PongScore(models.Model):
    """Class used to model a players score for pong.
    
        FIELDS:
            players         [One to One Field]
                            reference to a Player who this PongScore describes
                            (see models.Player in house app)
            games_played    [Integer Field]
                            total number of pong games played
            wins            [Integer Field]
                            total number of pong wins
            losses          [Integer Field]
                            total number of pool losses
            win_percent     [Float Field]
                            win percentage; wins / games_played
            mu              [Float Field]
                            mean value of normal distribution used to represent
                            a player's score; defaults to 25.0 upon initialization
            sigma           [Float Field]
                            standard deviation of normal distribution used to
                            represent a players score; defaults to 25.0 / 3 =
                            8.333333 upon initialization
            score           [Float Field]
                            score used to compare players; calculated using the
                            equation -> mu - 3 * sigma
    
    Note: fields such as losses, win_percent, and score are simply for convenience
    so they do not have to be calculated every time rankings are diplayed. These
    fields should only be calculated and updated when a game is added."""
    
    player = models.OneToOneField('house.Player')
    games_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    win_percent = models.FloatField(default=0)
    mu = models.FloatField(default=MU)
    sigma = models.FloatField(default=SIGMA)
    score = models.FloatField(default=MU - 3 * SIGMA)

    def publish(self):
        """Function to save the state of an instance of PoolScore to the
        database."""
        
        self.save()


class PongGame(models.Model):
    """Class used to model a players score for pong.
    
        FIELDS:
            winner1     [Foreign Key]
                        reference to the player who was the first winner
            winner2     [Foreign Key] (can be blank)
                        reference to the player who was the second winner
            loser1      [Foreign Key]
                        reference to the player who was the first loser
            loser2      [Foreign Key] (can be blank)
                        reference to the player who was the second loser
            date        [Date Field]
                        date the game was played
    
    Note: winner2 and loser2 can be null or blank as games can be 1v1, 1v2 or 2v2"""
    
    winner1 = models.ForeignKey('house.Player', related_name='pong_winner1')
    winner2 = models.ForeignKey('house.Player', related_name='pong_winner2',
        blank=True, null=True)
    loser1 = models.ForeignKey('house.Player', related_name='pong_loser1')
    loser2 = models.ForeignKey('house.Player', related_name='pong_loser2',
        blank=True, null=True)
    date = models.DateField()
    percent = models.FloatField()

    def publish(self):
        """Function to save the state of an instance of PoolScore to the
        database."""
        
        self.save()
