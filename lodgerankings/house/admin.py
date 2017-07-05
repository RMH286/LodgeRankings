from django.contrib import admin
from .models import Player
from pool_rank.models import PoolScore
from pong_rank.models import PongScore
from xbox_rank.models import XboxScore

# Register your models here.


class PoolScoreInline(admin.StackedInline):
    model = PoolScore


class PongScoreInline(admin.StackedInline):
    model = PongScore


class XboxScoreInline(admin.StackedInline):
    model = XboxScore


class PlayerAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'netid']
    inlines = [PoolScoreInline, PongScoreInline, XboxScoreInline]


admin.site.register(Player, PlayerAdmin)