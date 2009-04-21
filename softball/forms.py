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
    at_bats = self.cleaned_data.get("at_bats", 0)
    walks = self.cleaned_data.get("walks", 0)
    singles = self.cleaned_data.get("singles", 0)
    doubles = self.cleaned_data.get("doubles", 0)
    triples = self.cleaned_data.get("triples", 0)
    home_runs = self.cleaned_data.get("home_runs", 0)
    hits = singles + doubles + triples + home_runs
    if hits > at_bats:
        self._errors["at_bats"] = ErrorList(["At bats must be greater than or equal to hits"])
    return super(self.__class__, self).clean()

GameStatisticFormSet.form.clean = clean
PlayerStatisticFormSet.form.clean = clean
