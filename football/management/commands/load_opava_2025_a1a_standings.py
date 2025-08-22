from django.core.management.base import BaseCommand
from django.db import transaction
from football.models import League, Team, Standing


TABLE_NAME = "Opava A1A - 8.liga - PŘEBOR MUŽI"
SEASON = "2025"


STANDINGS = [
    # position, club, played, won, drawn, lost, goals_for, goals_against, points
    (1,  "Raduň",           1, 1, 0, 0, 5, 2, 3),
    (2,  "Kravaře \"B\"",  1, 1, 0, 0, 3, 1, 3),
    (3,  "Šilheřovice",     1, 1, 0, 0, 3, 1, 3),
    (4,  "Kozmice \"B\"",   1, 1, 0, 0, 3, 2, 3),
    (5,  "Komárov",         1, 1, 0, 0, 3, 2, 3),
    (6,  "Žimrovice",       1, 1, 0, 0, 1, 0, 3),
    (7,  "Chuchelná",       1, 0, 1, 0, 3, 3, 1),
    (8,  "Stěbořice",       1, 0, 1, 0, 3, 3, 1),
    (9,  "Velké Hoštice",   1, 0, 0, 1, 2, 3, 0),
    (10, "Kylešovice",      1, 0, 0, 1, 2, 3, 0),
    (11, "Otice",           1, 0, 0, 1, 0, 1, 0),
    (12, "Těškovice",       1, 0, 0, 1, 1, 3, 0),
    (13, "Hlavnice",        1, 0, 0, 1, 1, 3, 0),
    (14, "Slavkov \"B\"",  1, 0, 0, 1, 2, 5, 0),
]


class Command(BaseCommand):
    help = (
        "Load standings for 'Opava A1A - 8.liga - PŘEBOR MUŽI' (2025) into the Standings table.\n"
        "Creates the League and Teams if missing. Existing standings for this league are overwritten."
    )

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Do not write to DB, only print actions")
        parser.add_argument("--league-name", default=TABLE_NAME, help="League name (defaults to the built-in name)")
        parser.add_argument("--season", default=SEASON, help="Season string (defaults to 2025)")

    def _find_hlavnice_team(self):
        # Try to reuse existing club team to avoid duplicates
        t = Team.objects.filter(is_club_team=True).first()
        return t

    @transaction.atomic
    def handle(self, *args, **opts):
        dry = opts.get("dry_run", False)
        name = opts.get("league_name")
        season = opts.get("season")

        league, created = League.objects.get_or_create(name=name, season=season)
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created League: {league}"))
        else:
            # NOTICE style may not exist on older Django; fallback to SUCCESS
            try:
                self.stdout.write(self.style.NOTICE(f"Using existing League: {league}"))
            except Exception:
                self.stdout.write(self.style.SUCCESS(f"Using existing League: {league}"))

        # Overwrite existing standings for this league (safe to clear before insert)
        existing_count = Standing.objects.filter(league=league).count()
        if existing_count:
            if dry:
                self.stdout.write(self.style.WARNING(f"[dry-run] Would delete {existing_count} existing standings for {league}"))
            else:
                Standing.objects.filter(league=league).delete()
                self.stdout.write(self.style.WARNING(f"Deleted {existing_count} existing standings for {league}"))

        club_team = self._find_hlavnice_team()

        for pos, club_name, played, won, drawn, lost, gf, ga, pts in STANDINGS:
            # Use dedicated handling for Hlavnice to avoid duplicate records
            team = None
            if club_name.strip().lower().startswith("hlavnice"):
                team = club_team
            if team is None:
                team, t_created = Team.objects.get_or_create(name=club_name, defaults={"is_club_team": False})
                # Ensure team is linked to the league for convenience
                if team.league_id != league.id:
                    team.league = league
                    if not dry:
                        team.save()
                if t_created:
                    self.stdout.write(self.style.SUCCESS(f"Created team '{team.name}'"))
            else:
                # If we reused the club team, make sure it's assigned to league
                if team.league_id != league.id:
                    team.league = league
                    if not dry:
                        team.save()

            if dry:
                self.stdout.write(
                    f"[dry-run] Would upsert Standing for {team.name}: pos={pos}, Z={played}, V={won}, R={drawn}, P={lost}, {gf}:{ga}, B={pts}"
                )
                continue

            Standing.objects.create(
                team=team,
                league=league,
                position=pos,
                played=played,
                won=won,
                drawn=drawn,
                lost=lost,
                goals_for=gf,
                goals_against=ga,
                points=pts,
            )

        self.stdout.write(self.style.SUCCESS("Standings loaded successfully."))
