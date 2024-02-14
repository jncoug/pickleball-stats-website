from django import forms
from .models import Match, Player, Team


class CustomMatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = "__all__"

    players = forms.ModelMultipleChoiceField(
        queryset=Player.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
