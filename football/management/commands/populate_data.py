from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from football.models import (
    ClubInfo, League, Team, Player, Management, News, 
    Match, Standing, Event, MainPage
)

class Command(BaseCommand):
    help = 'Populate database with sample data for TJ Hlavnice'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data for TJ Hlavnice...')
        
        # Create club info
        club_info, created = ClubInfo.objects.get_or_create(
            name="TJ Družba Hlavnice",
            defaults={
                'founded_year': 1952,
                'history': 'TJ Družba Hlavnice byl založen v roce 1952 a je jedním z nejstarších fotbalových klubů v regionu. Klub má bohatou tradici a v průběhu let vychoval mnoho talentovaných hráčů.',
                'address': 'Hlavnice 123\n123 45 Hlavnice',
                'contact_email': 'info@tjhlavnice.cz',
                'contact_phone': '+420 123 456 789'
            }
        )
        if created:
            self.stdout.write('✓ Club info created')
        
        # Create league
        league, created = League.objects.get_or_create(
            name="Krajská soutěž",
            season="2024/2025",
            defaults={
                'description': 'Krajská fotbalová soutěž pro sezónu 2024/2025'
            }
        )
        if created:
            self.stdout.write('✓ League created')
        
        # Create teams
        teams_data = [
            {'name': 'TJ Družba Hlavnice', 'city': 'Hlavnice', 'is_club_team': True},
            {'name': 'FK Rosice', 'city': 'Rosice', 'is_club_team': False},
            {'name': 'TJ Sokol Kuřim', 'city': 'Kuřim', 'is_club_team': False},
            {'name': 'SK Líšeň', 'city': 'Brno', 'is_club_team': False},
            {'name': 'FC Zbrojovka Brno B', 'city': 'Brno', 'is_club_team': False},
            {'name': 'TJ Tatran Bohunice', 'city': 'Bohunice', 'is_club_team': False},
            {'name': 'FK Blansko', 'city': 'Blansko', 'is_club_team': False},
            {'name': 'TJ Olympia Ráječko', 'city': 'Ráječko', 'is_club_team': False},
        ]
        
        teams = {}
        for team_data in teams_data:
            team, created = Team.objects.get_or_create(
                name=team_data['name'],
                defaults={
                    'city': team_data['city'],
                    'league': league,
                    'is_club_team': team_data['is_club_team'],
                    'founded': 1952 if team_data['is_club_team'] else None
                }
            )
            teams[team_data['name']] = team
            if created:
                self.stdout.write(f'✓ Team {team.name} created')
        
        club_team = teams['TJ Družba Hlavnice']
        
        # Create players for club team
        players_data = [
            {'number': 1, 'first': 'Jan', 'last': 'Novák', 'position': 'GK'},
            {'number': 2, 'first': 'Petr', 'last': 'Svoboda', 'position': 'DEF'},
            {'number': 3, 'first': 'Martin', 'last': 'Dvořák', 'position': 'DEF'},
            {'number': 4, 'first': 'Tomáš', 'last': 'Černý', 'position': 'DEF'},
            {'number': 5, 'first': 'Pavel', 'last': 'Procházka', 'position': 'DEF'},
            {'number': 6, 'first': 'Jiří', 'last': 'Krejčí', 'position': 'MID'},
            {'number': 7, 'first': 'Lukáš', 'last': 'Horáček', 'position': 'MID'},
            {'number': 8, 'first': 'David', 'last': 'Mareš', 'position': 'MID'},
            {'number': 9, 'first': 'Michal', 'last': 'Veselý', 'position': 'FWD'},
            {'number': 10, 'first': 'Adam', 'last': 'Krejčí', 'position': 'FWD'},
            {'number': 11, 'first': 'Filip', 'last': 'Hrubý', 'position': 'FWD'},
        ]
        
        for player_data in players_data:
            player, created = Player.objects.get_or_create(
                team=club_team,
                jersey_number=player_data['number'],
                defaults={
                    'first_name': player_data['first'],
                    'last_name': player_data['last'],
                    'position': player_data['position'],
                    'birth_date': datetime(1995, 1, 1).date(),
                    'goals': 0,
                    'yellow_cards': 0,
                    'red_cards': 0
                }
            )
            if created:
                self.stdout.write(f'✓ Player {player.full_name} created')
        
        # Create management team
        management_data = [
            {'first': 'Karel', 'last': 'Novotný', 'role': 'PRESIDENT'},
            {'first': 'Jindřich', 'last': 'Svoboda', 'role': 'COACH'},
            {'first': 'Miroslav', 'last': 'Dvořák', 'role': 'ASSISTANT'},
            {'first': 'Anna', 'last': 'Krásná', 'role': 'TREASURER'},
            {'first': 'Petra', 'last': 'Malá', 'role': 'SECRETARY'},
        ]
        
        for i, mgmt_data in enumerate(management_data):
            mgmt, created = Management.objects.get_or_create(
                first_name=mgmt_data['first'],
                last_name=mgmt_data['last'],
                defaults={
                    'role': mgmt_data['role'],
                    'order': i + 1,
                    'bio': f'Zkušený člen vedení klubu TJ Družba Hlavnice.',
                }
            )
            if created:
                self.stdout.write(f'✓ Management {mgmt.first_name} {mgmt.last_name} created')
        
        # Create news articles
        admin_user = User.objects.get(username='admin')
        news_data = [
            {
                'title': 'Vítejte na nových webových stránkách TJ Družba Hlavnice!',
                'content': 'S radostí vám představujeme nové webové stránky našeho klubu. Najdete zde všechny aktuální informace o zápasech, výsledcích, sestavě týmu a dalších aktivitách klubu. Sledujte naše aktuality a buďte v obraze!',
                'is_featured': True
            },
            {
                'title': 'Začátek nové sezóny 2024/2025',
                'content': 'Nová sezóna je tady! Tým TJ Družba Hlavnice se pilně připravuje na nadcházející zápasy. Příprava probíhá podle plánu a hráči jsou v dobré kondici. Věříme v úspěšnou sezónu!',
                'is_featured': False
            },
            {
                'title': 'Pozvánka na domácí zápas',
                'content': 'Zveme všechny příznivce na náš příští domácí zápas. Přijďte podpořit náš tým a prožijte skvělou fotbalovou atmosféru. Vstup volný!',
                'is_featured': False
            }
        ]
        
        for news_item in news_data:
            news, created = News.objects.get_or_create(
                title=news_item['title'],
                defaults={
                    'content': news_item['content'],
                    'author': admin_user,
                    'is_featured': news_item['is_featured'],
                    'published': True
                }
            )
            if created:
                self.stdout.write(f'✓ News "{news.title}" created')
        
        # Create standings
        standings_data = [
            {'team': 'FC Zbrojovka Brno B', 'position': 1, 'played': 10, 'won': 8, 'drawn': 1, 'lost': 1, 'gf': 25, 'ga': 8, 'points': 25},
            {'team': 'SK Líšeň', 'position': 2, 'played': 10, 'won': 7, 'drawn': 2, 'lost': 1, 'gf': 22, 'ga': 10, 'points': 23},
            {'team': 'FK Blansko', 'position': 3, 'played': 10, 'won': 6, 'drawn': 3, 'lost': 1, 'gf': 18, 'ga': 9, 'points': 21},
            {'team': 'TJ Družba Hlavnice', 'position': 4, 'played': 10, 'won': 5, 'drawn': 3, 'lost': 2, 'gf': 16, 'ga': 12, 'points': 18},
            {'team': 'TJ Sokol Kuřim', 'position': 5, 'played': 10, 'won': 5, 'drawn': 2, 'lost': 3, 'gf': 15, 'ga': 13, 'points': 17},
            {'team': 'FK Rosice', 'position': 6, 'played': 10, 'won': 4, 'drawn': 2, 'lost': 4, 'gf': 12, 'ga': 15, 'points': 14},
            {'team': 'TJ Tatran Bohunice', 'position': 7, 'played': 10, 'won': 2, 'drawn': 3, 'lost': 5, 'gf': 10, 'ga': 18, 'points': 9},
            {'team': 'TJ Olympia Ráječko', 'position': 8, 'played': 10, 'won': 1, 'drawn': 2, 'lost': 7, 'gf': 8, 'ga': 21, 'points': 5},
        ]
        
        for standing_data in standings_data:
            team = teams[standing_data['team']]
            standing, created = Standing.objects.get_or_create(
                team=team,
                league=league,
                defaults={
                    'position': standing_data['position'],
                    'played': standing_data['played'],
                    'won': standing_data['won'],
                    'drawn': standing_data['drawn'],
                    'lost': standing_data['lost'],
                    'goals_for': standing_data['gf'],
                    'goals_against': standing_data['ga'],
                    'points': standing_data['points']
                }
            )
            if created:
                self.stdout.write(f'✓ Standing for {team.name} created')
        
        # Create some matches
        now = timezone.now()
        matches_data = [
            # Past matches
            {
                'home': 'TJ Družba Hlavnice',
                'away': 'FK Rosice',
                'date': now - timedelta(days=7),
                'home_score': 2,
                'away_score': 1,
                'location': 'Hlavnice'
            },
            {
                'home': 'TJ Sokol Kuřim',
                'away': 'TJ Družba Hlavnice',
                'date': now - timedelta(days=14),
                'home_score': 1,
                'away_score': 3,
                'location': 'Kuřim'
            },
            # Future matches
            {
                'home': 'TJ Družba Hlavnice',
                'away': 'SK Líšeň',
                'date': now + timedelta(days=7),
                'home_score': None,
                'away_score': None,
                'location': 'Hlavnice'
            },
            {
                'home': 'FK Blansko',
                'away': 'TJ Družba Hlavnice',
                'date': now + timedelta(days=14),
                'home_score': None,
                'away_score': None,
                'location': 'Blansko'
            }
        ]
        
        for match_data in matches_data:
            home_team = teams[match_data['home']]
            away_team = teams[match_data['away']]
            match, created = Match.objects.get_or_create(
                home_team=home_team,
                away_team=away_team,
                date=match_data['date'],
                defaults={
                    'league': league,
                    'home_score': match_data['home_score'],
                    'away_score': match_data['away_score'],
                    'location': match_data['location']
                }
            )
            if created:
                self.stdout.write(f'✓ Match {match} created')
        
        # Create main page configuration
        main_page, created = MainPage.objects.get_or_create()
        if created:
            self.stdout.write('✓ Main page configuration created')
        
        # Create an event
        event, created = Event.objects.get_or_create(
            title="Tréninky mládeže",
            defaults={
                'description': 'Pravidelné tréninky mládežnických kategorií.',
                'date': now + timedelta(days=2),
                'location': 'Sportovní areál Hlavnice',
                'is_match': False
            }
        )
        if created:
            self.stdout.write('✓ Event created')
        
        self.stdout.write(
            self.style.SUCCESS('Sample data created successfully!')
        )
