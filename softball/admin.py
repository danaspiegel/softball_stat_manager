from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.contenttypes import generic

from softball.models import *

class PlayerAdmin(admin.ModelAdmin):
    ordering = ("last_name", )
    list_display = ("first_name", "last_name", "number", )
admin.site.register(Player, PlayerAdmin)

class GameAdmin(admin.ModelAdmin):
    ordering = ("game_date", )
    list_display = ("game_date", "opponent", "score", "opponent_score", )
admin.site.register(Game, GameAdmin)

class StatisticAdmin(admin.ModelAdmin):
    ordering = ("created_on", )
    list_display = ("player", "game", "at_bats", "runs", "hits", "doubles", "triples", "home_runs", "rbis", "walks", )
admin.site.register(Statistic, StatisticAdmin)
