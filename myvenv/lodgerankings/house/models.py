from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Player(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    netid = models.CharField(max_length=10, primary_key=True)

    def publish(self):
        self.save()

    def __str__(self):
        return self.first_name + ' ' + self.last_name
