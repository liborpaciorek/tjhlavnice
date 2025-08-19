from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.db.models import Q
from .models import (
    ClubInfo, News, Team, Player, Management, Match, 
    Standing, Event, Gallery, MainPage, League
)

def home(request):
    """Main page view"""
    try:
        main_page = MainPage.objects.first()
        if not main_page:
            main_page = MainPage.objects.create()
    except:
        main_page = None
    
    context = {
        'latest_news': News.objects.filter(published=True)[:3],
        'upcoming_match': None,
        'recent_matches': [],
        'club_standing': [],
        'club_info': ClubInfo.objects.first(),
    }
    
    if main_page:
        context.update({
            'upcoming_match': main_page.get_upcoming_match(),
            'recent_matches': main_page.get_recent_matches(),
            'club_standing': main_page.get_club_standing(),
        })
    
    return render(request, 'football/home.html', context)

class NewsListView(ListView):
    model = News
    template_name = 'football/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10
    
    def get_queryset(self):
        try:
            return News.objects.filter(published=True)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error fetching news: {e}")
            return News.objects.none()

class NewsDetailView(DetailView):
    model = News
    template_name = 'football/news_detail.html'
    context_object_name = 'news'
    
    def get_queryset(self):
        try:
            return News.objects.filter(published=True)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error fetching news detail: {e}")
            return News.objects.none()

def team_lineup(request):
    """Team lineup view"""
    club_team = Team.objects.filter(is_club_team=True).first()
    players = Player.objects.filter(team=club_team) if club_team else Player.objects.none()
    
    context = {
        'team': club_team,
        'goalkeepers': players.filter(position='GK'),
        'defenders': players.filter(position='DEF'),
        'midfielders': players.filter(position='MID'),
        'forwards': players.filter(position='FWD'),
    }
    return render(request, 'football/team_lineup.html', context)

def management(request):
    """Management team view"""
    management_team = Management.objects.all()
    return render(request, 'football/management.html', {'management_team': management_team})

class MatchListView(ListView):
    model = Match
    template_name = 'football/matches.html'
    context_object_name = 'matches'
    paginate_by = 20
    
    def get_queryset(self):
        return Match.objects.filter(
            Q(home_team__is_club_team=True) | Q(away_team__is_club_team=True)
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context['upcoming_matches'] = self.get_queryset().filter(date__gte=now)[:5]
        context['recent_matches'] = self.get_queryset().filter(date__lt=now, home_score__isnull=False)[:10]
        return context

def standings(request):
    """Display standings for all leagues."""
    standings_by_league = {}
    
    # Get all leagues with their standings
    for league in League.objects.all():
        league_standings = Standing.objects.filter(
            league=league
        ).select_related('team').order_by('position')
        
        if league_standings.exists():
            # Add calculated statistics to each standing
            for standing in league_standings:
                # Calculate success rate (percentage)
                max_points = standing.played * 3
                standing.success_rate = round((standing.points / max_points * 100) if max_points > 0 else 0, 1)
                
                # Calculate average goals per match
                standing.avg_goals_for = round((standing.goals_for / standing.played) if standing.played > 0 else 0, 1)
                standing.avg_goals_against = round((standing.goals_against / standing.played) if standing.played > 0 else 0, 1)
            
            standings_by_league[league] = league_standings
    
    context = {
        'standings_by_league': standings_by_league,
        'page_title': 'Tabulky'
    }
    return render(request, 'football/standings.html', context)

class EventListView(ListView):
    model = Event
    template_name = 'football/calendar.html'
    context_object_name = 'events'
    
    def get_queryset(self):
        return Event.objects.filter(date__gte=timezone.now())

class GalleryListView(ListView):
    model = Gallery
    template_name = 'football/gallery.html'
    context_object_name = 'photos'
    paginate_by = 12
    
    def get_queryset(self):
        try:
            return Gallery.objects.all()
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error fetching gallery: {e}")
            return Gallery.objects.none()

def club_info(request):
    """Club information view"""
    club = ClubInfo.objects.first()
    
    # Calculate years of existence
    if club and club.founded_year:
        from datetime import datetime
        current_year = datetime.now().year
        years_of_existence = current_year - club.founded_year
    else:
        years_of_existence = 0
    
    context = {
        'club': club,
        'years_of_existence': years_of_existence
    }
    return render(request, 'football/club_info.html', context)
