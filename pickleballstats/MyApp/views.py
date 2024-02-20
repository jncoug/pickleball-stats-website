from django.shortcuts import render
from django.db.models import F, Sum, Count, Avg
from .models import PlayerStats, Player, Match, Tournament
from datetime import date


# Functions
# Combine all stats for all PlayerStats Objects
def aggregate_stats(player_query_set):

    aggregated_stats = player_query_set.annotate(
        total_matches=Count("match"),
        total_rallies_played=Sum("rallies_played"),
        total_rallies_won=Sum("rallies_won"),
        rally_win_percentage=100 * F("rallies_won") / F("rallies_played"),
        total_points_won=Sum("points_won"),
        total_serves=Sum("serves"),
        total_serves_won=Sum("serve_winners"),
        serve_win_percentage=100 * F("serve_winners") / F("serves"),
        total_serves_missed=Sum("serve_misses"),
        serve_miss_percentage=100 * F("serve_misses") / F("serves"),
        total_returns=Sum("returns"),
        total_returns_missed=Sum("return_misses"),
        return_miss_percentage=100 * F("return_misses") / F("returns"),
        total_returns_won=Sum("return_winners"),
        return_win_percentage=100 * F("return_winners") / F("returns"),
        total_thirds=Sum("thirds"),
        total_third_drops=Sum("third_drops"),
        third_drop_percentage=100 * F("third_drops") / F("thirds"),
        total_third_drives=Sum("third_drives"),
        third_drive_percentage=100 * F("third_drives") / F("thirds"),
        total_third_drop_makes=Sum("third_drop_makes"),
        third_drop_make_percentage=100 * F("third_drop_makes") / F("third_drops"),
        total_third_drop_winners=Sum("third_drop_winners"),
        total_third_drop_misses=Sum("third_drop_misses"),
        third_drop_miss_percentage=100 * F("third_drop_misses") / F("third_drops"),
        total_drives=Sum("drives"),
        total_drives_won=Sum("drive_winners"),
        drive_win_percentage=100 * F("drive_winners") / F("drives"),
        total_drives_missed=Sum("drive_misses"),
        drive_miss_percentage=100 * F("drive_misses") / F("drives"),
        total_drives_lost=Sum("drive_losers"),
        drive_loss_percentage=100 * F("drive_losers") / F("drives"),
        total_dink_misses=Sum("dink_misses"),
        total_dink_winners=Sum("dink_winners"),
        total_volley_speed_ups=Sum("volley_speed_ups"),
        total_volley_speed_ups_won=Sum("volley_speed_up_winners"),
        volley_speed_up_win_percentage=100
        * F("volley_speed_up_winners")
        / F("volley_speed_ups"),
        total_volley_speed_ups_missed=Sum("volley_speed_up_misses"),
        volley_speed_up_miss_percentage=100
        * F("volley_speed_up_misses")
        / F("volley_speed_ups"),
        total_off_bounce_speed_ups=Sum("off_bounce_speed_ups"),
        total_off_bounce_speed_ups_won=Sum("off_bounce_speed_up_winners"),
        off_bounce_speed_up_win_percentage=100
        * F("off_bounce_speed_up_winners")
        / F("off_bounce_speed_ups"),
        total_off_bounce_speed_ups_missed=Sum("off_bounce_speed_up_misses"),
        off_bounce_speed_up_miss_percentage=100
        * F("off_bounce_speed_up_misses")
        / F("off_bounce_speed_ups"),
        total_counters=Sum("counters"),
        total_counters_won=Sum("counter_winners"),
        counter_win_percentage=100 * F("counter_winners") / F("counters"),
        total_counters_missed=Sum("counter_misses"),
        counter_miss_percentage=100 * F("counter_misses") / F("counters"),
        total_counters_lost=Sum("counter_losers"),
        counter_loss_percentage=100 * F("counter_losers") / F("counters"),
        total_resets=Sum("resets"),
        total_resets_made=Sum("resets_made"),
        reset_made_percentage=100 * F("resets_made") / F("resets"),
        total_resets_missed=Sum("resets_missed"),
        reset_miss_percentage=100 * F("resets_missed") / F("resets"),
        total_lobs=Sum("lobs"),
        total_lobs_made=Sum("lob_successes"),
        lob_made_percentage=100 * F("lob_successes") / F("lobs"),
        total_lobs_won=Sum("lob_winners"),
        lob_win_percentage=100 * F("lob_winners") / F("lobs"),
        total_lobs_missed=Sum("lob_misses"),
        lob_miss_percentage=F("lob_misses") / F("lobs"),
        total_lobs_lost=Sum("lob_losers"),
        lob_lose_percentage=100 * F("lob_losers") / F("lobs"),
        total_popups=Sum("popups"),
        total_popups_lost=Sum("popup_losers"),
        popup_lose_percentage=100 * F("popup_losers") / F("popups"),
        total_putaways=Sum("putaway_attempts"),
        total_putaways_won=Sum("putaway_winners"),
        putaway_win_percentage=100 * F("putaway_winners") / F("putaway_attempts"),
        total_putaways_missed=Sum("putaway_misses"),
        putaway_miss_percentage=100 * F("putaway_misses") / F("putaway_attempts"),
        total_atps=Sum("atps"),
        total_atps_won=Sum("atp_winners"),
        atp_win_percentage=100 * F("atp_winners") / F("atps"),
        total_atps_missed=Sum("atp_misses"),
        atp_miss_percentage=100 * F("atp_misses") / F("atps"),
        total_ernes=Sum("ernes"),
        total_ernes_won=Sum("erne_winners"),
        erne_win_percentage=100 * F("erne_winners") / F("ernes"),
        total_ernes_missed=Sum("erne_misses"),
        erne_miss_percentage=100 * F("erne_misses") / F("ernes"),
        total_nvz_faults=Sum("nvz_faults"),
        total_service_faults=Sum("service_faults"),
        total_technical_warnings=Sum("technical_warnings"),
    )

    return aggregated_stats


# calculate age from birth year
def get_age_from_birthdate(birthdate):
    byear, bmonth, bday = map(int, str(birthdate).split("-"))
    tyear, tmonth, tday = map(int, str(date.today()).split("-"))

    return tyear - byear - ((tmonth, tday) < (bmonth, bday))


# VIEWS.
def home_page(request):
    return render(request, "index.html")


# Player Page Stats
def player_page_stats(request):
    player_id = request.GET.get("player_id", 3)
    queryset = PlayerStats.objects.filter(player__pk=player_id)

    aggregated_stats = aggregate_stats(queryset)
    player_info = Player.objects.filter(id=player_id)[0]
    # next_player = Player.objects.filter(id=str(int(player_id) + 1))[0]
    # prev_player = Player.objects.filter(id=str(int(player_id) - 1))[0]

    # get age of player by birthdate
    age = get_age_from_birthdate(player_info.birthdate)

    # This is filtering to accept the first queryset
    if aggregated_stats:
        stats_data = aggregated_stats[0]
    else:
        stats_data = {}  # Handle case where the player has no stats

    context = {
        "stats": stats_data,
        "player": player_info,
        "age": age,
    }
    return render(request, "player.html", context)


# LEADERBOARD
def leaderboards(request):
    year_filter = request.GET.get("year", None)  # placeholder
    sex_filter = request.GET.get("sex", None)  # placeholder
    bracket_filter = request.GET.get("bracket", None)

    order_by_field = request.GET.get("order_by", "-serve_winners")  # Default sorting

    queryset = PlayerStats.objects.all()

    if year_filter:
        queryset = queryset.filter(match__date__year=year_filter)

    if sex_filter:
        queryset = queryset.filter(player__sex=sex_filter)

    if bracket_filter:
        queryset = queryset.filter(match__bracket=bracket_filter)

    queryset = queryset.order_by(order_by_field)

    aggregated_stats = aggregate_stats(queryset)

    context = {"aggregated_stats": aggregated_stats}

    return render(request, "leaderboards.html", context)


# order players by serve winner percentage
def get_stats_by_serve_winner_percentage(request):
    player_stats = PlayerStats.objects.annotate(
        serve_winner_pct=100 * F("serve_winners") / F("serves")
    ).order_by("-serve_winner_pct")

    context = {"player_stats_list": player_stats}

    return render(request, "stats/player_stats_list.html", context)
