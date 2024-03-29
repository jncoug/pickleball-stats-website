from django.db import models
from django.core.exceptions import ValidationError
import pdb

# Create your models here.


class Tournament(models.Model):
    name = models.CharField(max_length=200)
    host = models.CharField(
        max_length=3,
        choices=[
            ("PPA", "Professional Pickelball Association"),
            ("MLP", "Major League Pickleball"),
            ("APP", "Association of Pickleball Professionals"),
        ],
    )
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.host}"


class Player(models.Model):
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    birthdate = models.DateField()
    sex = models.CharField(max_length=1, choices=[("M", "Male"), ("F", "Female")])
    hand = models.CharField(max_length=1, choices=[("R", "Right"), ("L", "Left")])
    turned_pro = models.CharField(max_length=4)
    sponsor = models.CharField(max_length=100)
    bracket = models.CharField(
        max_length=2,
        choices=[("MS", "Mens Singles"), ("WS", "Women's Singles")],
    )

    def __str__(self):
        return f"{self.f_name} {self.l_name}"


class Match(models.Model):
    class GameCount(models.IntegerChoices):
        ONE = 1, "Best of 1"
        THREE = 3, "Best of 3"
        FIVE = 5, "Best of 5"

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    date = models.DateField()
    bracket = models.CharField(
        max_length=3,
        choices=[
            ("MS", "Men's Singles"),
            ("MD", "Men's Doubles"),
            ("MXD", "Mixed Doubles"),
            ("WD", "Women's Doubles"),
            ("WS", "Women's Singles"),
        ],
    )
    round = models.CharField(
        max_length=3,
        choices=[
            ("QLF", "Qualifier"),
            ("R64", "Round of 64"),
            ("R32", "Round of 32"),
            ("R16", "Round of 16"),
            ("QF", "Quarter Finals"),
            ("SF", "Semi Finals"),
            ("GLD", "Gold Medal Match"),
            ("BRZ", "Bronze Medal Match"),
        ],
    )
    players = models.ManyToManyField(Player, blank=True)
    game_count = models.IntegerField(choices=GameCount.choices)
    scoring_type = models.CharField(
        max_length=8,
        choices=[
            ("Side Out", "Side out scoring"),
            ("Rally", "Rally scoring"),
        ],
    )
    # winning_team
    # winning_points = points
    # losing... etc.

    def __str__(self):
        if self.pk is not None:
            self_with_players = Match.objects.prefetch_related("players").get(
                pk=self.pk
            )
            player_count = len(self_with_players.players.all())

            if player_count >= 2:
                # It's a singles match
                player_names = ", ".join([str(player) for player in self.players.all()])
                return f"{self.round} {self.get_bracket_display()} match - {str(self.tournament)}"

        else:
            # Handle other cases or customize as needed
            return f"New match on {self.match_date.date()}"

    def clean(self):
        super().clean()
        # self.validate_players_by_bracket

    def validate_players_by_bracket(self):
        for player in self.players.all():
            if player.bracket != self.bracket:
                raise ValidationError(
                    f"Invalid player {str(player)}. Expected a {self.bracket} player, got a {player.bracket} player."
                )


class PlayerStats(models.Model):
    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="player_with_stats"
    )
    partner = models.ForeignKey(
        Player,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="partner_for_player",
    )
    opponent1 = models.ForeignKey(
        Player,
        on_delete=models.DO_NOTHING,
        related_name="opponent1",
    )
    opponent2 = models.ForeignKey(
        Player,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="opponent2_optional",
    )
    match = models.ForeignKey(Match, on_delete=models.CASCADE)

    # General statistics
    rallies_played = models.IntegerField(default=0)
    rallies_won = models.IntegerField(default=0)
    points_won = models.IntegerField(default=0)

    # Shot-specific counts and outcomes

    # serves
    serves = models.IntegerField(default=0)
    serve_winners = models.IntegerField(default=0)
    serve_losers = models.IntegerField(default=0)
    serve_neutrals = models.IntegerField(default=0)
    serve_misses = models.IntegerField(default=0)

    # returns
    returns = models.IntegerField(default=0)
    return_winners = models.IntegerField(default=0)
    return_losers = models.IntegerField(default=0)
    return_neutrals = models.IntegerField(default=0)
    return_misses = models.IntegerField(default=0)

    # 3rd shots
    thirds = models.IntegerField(default=0)
    third_drops = models.IntegerField(default=0)
    third_drives = models.IntegerField(default=0)

    # drops
    third_drop_makes = models.IntegerField(default=0)
    third_drop_winners = models.IntegerField(default=0)
    third_drop_misses = models.IntegerField(default=0)

    # drives - a drive attack from behind 50% of the court - typically on a 3rd shot
    drives = models.IntegerField(default=0)
    drive_winners = models.IntegerField(default=0)
    drive_losers = models.IntegerField(default=0)
    drive_neutrals = models.IntegerField(default=0)
    drive_misses = models.IntegerField(default=0)

    # dinks
    dink_winners = models.IntegerField(default=0)
    dink_misses = models.IntegerField(default=0)

    # volley speed ups - attacking a neutral ball with a volley
    volley_speed_ups = models.IntegerField(default=0)
    volley_speed_up_winners = models.IntegerField(default=0)
    volley_speed_up_losers = models.IntegerField(default=0)
    volley_speed_up_neutrals = models.IntegerField(default=0)
    volley_speed_up_misses = models.IntegerField(default=0)

    # off bounce speed ups- attacking a neutral ball with an off bounce shot
    off_bounce_speed_ups = models.IntegerField(default=0)
    off_bounce_speed_up_winners = models.IntegerField(default=0)
    off_bounce_speed_up_losers = models.IntegerField(default=0)
    off_bounce_speed_up_neutrals = models.IntegerField(default=0)
    off_bounce_speed_up_misses = models.IntegerField(default=0)

    # counters - the response to a speed up
    counters = models.IntegerField(default=0)
    counter_winners = models.IntegerField(default=0)
    counter_losers = models.IntegerField(default=0)
    counter_neutrals = models.IntegerField(default=0)
    counter_misses = models.IntegerField(default=0)

    # the direct and immediate neutralization of a speed up or put away
    resets = models.IntegerField(default=0)
    resets_made = models.IntegerField(default=0)
    resets_missed = models.IntegerField(default=0)

    # lobs
    lobs = models.IntegerField(default=0)
    lob_successes = models.IntegerField(default=0)
    lob_winners = models.IntegerField(default=0)
    lob_losers = models.IntegerField(default=0)
    lob_neutrals = models.IntegerField(default=0)
    lob_misses = models.IntegerField(default=0)

    # popups
    popups = models.IntegerField(default=0)
    popup_winners = models.IntegerField(
        default=0
    )  # this should almost never happen, very rare
    popup_losers = models.IntegerField(default=0)
    popup_neutrals = models.IntegerField(default=0)
    # no popup miss count because by definition it leads to a putaway attempt

    # putaway attempts
    putaway_attempts = models.IntegerField(default=0)
    putaway_winners = models.IntegerField(default=0)
    # no losers that doesn't make sense putaway_losers = models.IntegerField(default=0)
    putaway_neutrals = models.IntegerField(default=0)
    putaway_misses = models.IntegerField(default=0)

    # ernes and atps
    ernes = models.IntegerField(default=0)
    erne_winners = models.IntegerField(default=0)
    erne_neutrals = models.IntegerField(default=0)
    erne_misses = models.IntegerField(default=0)
    erne_losers = models.IntegerField(default=0)

    atps = models.IntegerField(default=0)
    atp_winners = models.IntegerField(default=0)
    atp_neutrals = models.IntegerField(default=0)
    atp_misses = models.IntegerField(default=0)
    atp_losers = models.IntegerField(default=0)

    # other
    nvz_faults = models.IntegerField(default=0)
    service_faults = models.IntegerField(default=0)
    technical_warnings = models.IntegerField(default=0)

    def __str__(self):
        if self.opponent2:
            return f"{str(self.player)} stats vs {str(self.opponent1)}/{str(self.opponent2)} - {str(self.match)} "
        else:
            return f"{str(self.player)} stats vs {str(self.opponent1)} - {str(self.match)} "
