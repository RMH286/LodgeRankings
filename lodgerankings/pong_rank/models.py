from __future__ import unicode_literals

from django.db import models

# Create your models here.

MU = 25.0
SIGMA = 25.0 / 3.0


class PongScore(models.Model):
    player = models.OneToOneField('house.Player')
    games_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    win_percent = models.FloatField(default=0)
    mu = models.FloatField(default=MU)
    sigma = models.FloatField(default=SIGMA)
    score = models.FloatField(default=MU - 3 * SIGMA)

    def publish(self):
        self.save()


class PongGame(models.Model):
    winner1 = models.ForeignKey('house.Player', related_name='pong_winner1')
    winner2 = models.ForeignKey('house.Player', related_name='pong_winner2',
        blank=True, null=True)
    loser1 = models.ForeignKey('house.Player', related_name='pong_loser1')
    loser2 = models.ForeignKey('house.Player', related_name='pong_loser2',
        blank=True, null=True)
    date = models.DateField()
    percent = models.FloatField()

    def publish(self):
        self.save()
