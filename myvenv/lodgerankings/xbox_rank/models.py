from __future__ import unicode_literals

from django.db import models

# Create your models here.


MU = 25.0
SIGMA = 25.0 / 3.0


class XboxScore(models.Model):
    player = models.OneToOneField('house.Player')
    xbox_wins = models.IntegerField(default=0)
    xbox_losses = models.IntegerField(default=0)
    xbox_mu = models.FloatField(default=MU)
    xbox_sigma = models.FloatField(default=SIGMA)
    xbox_score = models.FloatField(default=MU - 3 * SIGMA)

    def publish(self):
        self.save()