from django.contrib import admin
from .models import *
from .forms import CustomMatchForm


# setup class from forms
class MatchAdmin(admin.ModelAdmin):
    form = CustomMatchForm


# Register your models here.
admin.site.register(Tournament)
admin.site.register(Player)
admin.site.register(Match, MatchAdmin)
admin.site.register(PlayerStats)
