from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Player(models.Model):
    """Class used to model a player.
    
        FIELDS:
            first_name      [Char Field]
                            player's first name
            last_name       [Char Field]
                            player's last name
            netid           [char Field]
                            player's netid; must be unique since it serves as
                            the primary key
    """
    
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    netid = models.CharField(max_length=10, primary_key=True)

    def publish(self):
        """Function to save the state of an instance of PoolScore to the
        database."""
        
        self.save()

    def __str__(self):
        """Overrides class' str() function"""
        
        return self.first_name + ' ' + self.last_name
