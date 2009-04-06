import random

from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
import django.contrib.auth

from softball.models import *
from softball.forms import *

def list(request):
    players = get_list_or_404(Player)
    return render_to_response("players/list.html", { "players": players }, context_instance=RequestContext(request))

def view(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    return render_to_response("players/view.html", { "player": player }, context_instance=RequestContext(request))

@login_required
def add(request):
    player = Player()
    if request.method == "POST":
        form = PlayerForm(request.POST, instance=player)
        if form.is_valid():
            player = form.save()
            request.user.message_set.create(message="Player %s created" % str(player))
            return HttpResponseRedirect(reverse("player_list"))
    else:
        form = PlayerForm(instance=player)
    return render_to_response("players/add.html", { "player": player, "form": form }, context_instance=RequestContext(request))

@login_required
def edit(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    if request.method == "POST":
        form = PlayerForm(request.POST, instance=player)
        statistic_formset = PlayerStatisticFormSet(request.POST, instance=player)
        if form.is_valid() and statistic_formset.is_valid():
            player = form.save()
            statistic_formset.save()
            request.user.message_set.create(message="Player %s updated" % str(player))
            return HttpResponseRedirect(reverse("player_view", kwargs={ "player_id": player.id }))
    else:
        form = PlayerForm(instance=player)
        statistic_formset = PlayerStatisticFormSet(instance=player)
    return render_to_response("players/edit.html", { "player": player, "form": form, "statistic_formset": statistic_formset }, context_instance=RequestContext(request))

@login_required
def delete(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    player.delete()
    request.user.message_set.create(message="Player %s deleted" % str(player))
    return HttpResponseRedirect(reverse("player_list"))
