from django import forms
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

class StatisticForm(forms.ModelForm):
    class Meta:
        model = Statistic

GameStatisticFormSet = inlineformset_factory(Game, Statistic, extra=10)
PlayerStatisticFormSet = inlineformset_factory(Player, Statistic, extra=2)
