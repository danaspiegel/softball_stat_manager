import random

from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from softball.models import *
from softball.forms import *

def list(request):
    games = Game.objects.all()
    return render_to_response("games/list.html", { "games": games, }, context_instance=RequestContext(request))

def view(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    return render_to_response("games/view.html", { "game": game }, context_instance=RequestContext(request))

@login_required
def add(request):
    game = Game()
    if request.method == "POST":
        form = GameForm(request.POST, instance=game)
        if form.is_valid():
            game = form.save()
            return HttpResponseRedirect(reverse("game_list"))
    else:
        form = GameForm(instance=game)
    return render_to_response("games/add.html", { "game": game, "form": form }, context_instance=RequestContext(request))

@login_required
def edit(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    if request.method == "POST":
        form = GameForm(request.POST, instance=game)
        statistic_formset = GameStatisticFormSet(request.POST, instance=game)
        if form.is_valid() and statistic_formset.is_valid():
            game = form.save()
            statistic_formset.save()
            return HttpResponseRedirect(reverse("game_view", kwargs={ "game_id": game.id }))
    else:
        form = GameForm(instance=game)
        statistic_formset = GameStatisticFormSet(instance=game)
    return render_to_response("games/edit.html", { "game": game, "form": form, "statistic_formset": statistic_formset }, context_instance=RequestContext(request))

@login_required
def delete(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    game.delete()
    request.user.message_set.create(message="Game %s deleted" % str(game))
    return HttpResponseRedirect(reverse("game_list"))
