from django import forms
from .models import Match, Player


class CustomMatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = "__all__"

    players = forms.ModelMultipleChoiceField(
        queryset=Player.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
