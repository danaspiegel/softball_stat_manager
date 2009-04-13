from django import forms
from django.forms.util import ErrorList
from django.forms.models import inlineformset_factory

from softball.models import *

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        exclude = ["players"]

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        # exclude = ["players"]

GameStatisticFormSet = inlineformset_factory(Game, Statistic, extra=10)
PlayerStatisticFormSet = inlineformset_factory(Player, Statistic, extra=2)

def clean(self):
    """ Check if at_bats is big enough """
    print "clean_at_bats"
    print self.cleaned_data
    at_bats = self.cleaned_data.get("at_bats", 0)
    walks = self.cleaned_data.get("walks", 0)
    hits = self.cleaned_data.get("hits", 0)
    doubles = self.cleaned_data.get("doubles", 0)
    triples = self.cleaned_data.get("triples", 0)
    home_runs = self.cleaned_data.get("home_runs", 0)
    total_hits = hits + doubles + triples + home_runs
    if (walks + total_hits) > at_bats or total_hits > at_bats or walks > at_bats:
        self._errors["at_bats"] = ErrorList(["At bats must be greater than or equal to walks, hits, doubles, triples, and home runs."])
    return super(self.__class__, self).clean()

GameStatisticFormSet.form.clean = clean
PlayerStatisticFormSet.form.clean = clean
