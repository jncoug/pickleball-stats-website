from django.shortcuts import render
from django.db.models import F
from .models import PlayerStats


# Create your views here.

# order players by serve winner percentage
def get_stats_by_serve_winner_percentage(request):
    player_stats = PlayerStats \
        .objects \
        .annotate(serve_winner_pct=100 * F('serve_winners') / F('serves')) \
        .order_by('-serve_winner_pct')

    context = {'player_stats_list': player_stats}

    return render(request, 'stats/player_stats_list.html', context)