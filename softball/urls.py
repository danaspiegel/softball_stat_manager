from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to
import django.contrib.auth.views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("softball.views",
    url(r"^$", redirect_to, {"url": "games/"}, name="softball_index"),
    url(r"^games/$", "game.list", name="game_list"),
    url(r"^games/add/$", "game.add", name="game_add"),
    url(r"^games/(?P<game_id>[0-9]+)/$", "game.view", name="game_view"),
    url(r"^games/(?P<game_id>[0-9]+)/edit/$", "game.edit", name="game_edit"),
    url(r"^games/(?P<game_id>[0-9]+)/delete/$", "game.delete", name="game_delete"),
    url(r"^players/$", "player.list", name="player_list"),
    url(r"^players/add/$", "player.add", name="player_add"),
    url(r"^players/(?P<player_id>[0-9]+)/$", "player.view", name="player_view"),
    url(r"^players/(?P<player_id>[0-9]+)/edit/$", "player.edit", name="player_edit"),
    url(r"^players/(?P<player_id>[0-9]+)/delete/$", "player.delete", name="player_delete"),
)

