from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
import requests
import json
from datetime import datetime, timedelta
from .models import (
    ClubInfo, News, Team, Player, Management, Match, 
    Standing, Event, Gallery, GalleryAlbum, MainPage, League, GoogleCalendarSettings
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
        'upcoming_matches': [],
        'recent_matches': [],
        'club_standing': [],
        'club_info': ClubInfo.objects.first(),
    }
    
    if main_page:
        upcoming_match = main_page.get_upcoming_match()
        context.update({
            'upcoming_match': upcoming_match,
            'upcoming_matches': [upcoming_match] if upcoming_match else [],
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
    
    def _club_matches_qs(self):
        return Match.objects.filter(
            Q(home_team__is_club_team=True) | Q(away_team__is_club_team=True)
        )

    def get_queryset(self):
        qs = self._club_matches_qs()
        # Optional filter by league via query param (?league=<id>)
        self.selected_league = None
        league_id = self.request.GET.get('league') or self.request.GET.get('league_id')
        if league_id:
            try:
                self.selected_league = League.objects.get(pk=int(league_id))
                qs = qs.filter(league=self.selected_league)
            except (ValueError, League.DoesNotExist):
                self.selected_league = None
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        filtered_qs = self.get_queryset()
        # Upcoming: soonest first (ascending) — show all
        context['upcoming_matches'] = (
            filtered_qs.filter(date__gte=now).order_by('date')
        )
        # Recent (played): latest first (descending) — show all with a recorded score
        context['recent_matches'] = (
            filtered_qs.filter(date__lt=now, home_score__isnull=False).order_by('-date')
        )
        # Provide leagues for filter dropdown (only leagues where club plays)
        base_qs = self._club_matches_qs()
        context['leagues'] = League.objects.filter(pk__in=base_qs.values_list('league_id', flat=True).distinct()).order_by('name', 'season')
        context['selected_league'] = getattr(self, 'selected_league', None)
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

class GalleryAlbumListView(ListView):
    model = GalleryAlbum
    template_name = 'football/gallery_albums.html'
    context_object_name = 'albums'
    paginate_by = 12
    
    def get_queryset(self):
        return GalleryAlbum.objects.all()

class GalleryAlbumDetailView(DetailView):
    model = GalleryAlbum
    template_name = 'football/gallery_album_detail.html'
    context_object_name = 'album'
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['photos'] = self.object.photos.all()
        return ctx

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


def fetch_google_calendar_events(calendar_id, api_key, max_results=50, show_past_events=True, past_events_days=30):
    """Fetch events from Google Calendar API"""
    try:
        # Set time boundaries
        now = datetime.now()
        if show_past_events:
            time_min = (now - timedelta(days=past_events_days)).isoformat() + 'Z'
        else:
            time_min = now.isoformat() + 'Z'
        
        # Google Calendar API endpoint
        url = 'https://www.googleapis.com/calendar/v3/calendars/{}/events'.format(calendar_id)
        
        params = {
            'key': api_key,
            'timeMin': time_min,
            'maxResults': max_results,
            'singleEvents': 'true',
            'orderBy': 'startTime'
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            events = []
            
            for item in data.get('items', []):
                # Parse event data
                event = {
                    'id': item.get('id'),
                    'summary': item.get('summary', 'Bez názvu'),
                    'description': item.get('description', ''),
                    'location': item.get('location', ''),
                    'start': None,
                    'end': None,
                    'all_day': False,
                    'html_link': item.get('htmlLink', ''),
                }
                
                # Parse start time
                start = item.get('start', {})
                if 'dateTime' in start:
                    event['start'] = datetime.fromisoformat(start['dateTime'].replace('Z', '+00:00'))
                    event['all_day'] = False
                elif 'date' in start:
                    event['start'] = datetime.strptime(start['date'], '%Y-%m-%d')
                    event['all_day'] = True
                
                # Parse end time
                end = item.get('end', {})
                if 'dateTime' in end:
                    event['end'] = datetime.fromisoformat(end['dateTime'].replace('Z', '+00:00'))
                elif 'date' in end:
                    event['end'] = datetime.strptime(end['date'], '%Y-%m-%d')
                
                events.append(event)
            
            return events, None
        else:
            # Enhanced error handling for different status codes
            error_details = ""
            try:
                error_response = response.json()
                if 'error' in error_response:
                    error_info = error_response['error']
                    error_details = f" - {error_info.get('message', 'Unknown error')}"
            except:
                pass
            
            if response.status_code == 403:
                error_msg = f"API Error 403: Přístup odmítnut{error_details}. Zkontrolujte API klíč a oprávnění kalendáře."
            elif response.status_code == 404:
                error_msg = f"API Error 404: Kalendář nenalezen{error_details}. Zkontrolujte ID kalendáře."
            elif response.status_code == 400:
                error_msg = f"API Error 400: Neplatný požadavek{error_details}. Zkontrolujte formát ID kalendáře."
            else:
                error_msg = f"API Error {response.status_code}{error_details}"
            
            return [], error_msg
    
    except requests.exceptions.RequestException as e:
        return [], f"Connection Error: {str(e)}"
    except Exception as e:
        return [], f"Error: {str(e)}"


def google_calendar_view(request):
    """Google Calendar view"""
    try:
        calendar_settings = GoogleCalendarSettings.objects.first()
    except GoogleCalendarSettings.DoesNotExist:
        calendar_settings = None
    
    events = []
    error_message = None
    
    if calendar_settings and calendar_settings.is_active:
        if calendar_settings.calendar_id and calendar_settings.api_key:
            events, error_message = fetch_google_calendar_events(
                calendar_settings.calendar_id,
                calendar_settings.api_key,
                calendar_settings.max_events,
                calendar_settings.show_past_events,
                calendar_settings.past_events_days
            )
            if error_message:
                messages.error(request, f"Nepodařilo se načíst kalendář: {error_message}")
        else:
            messages.warning(request, "Kalendář není správně nakonfigurován. Kontaktujte správce.")
    elif calendar_settings:
        messages.info(request, "Kalendář je momentálně deaktivován.")
    else:
        messages.warning(request, "Kalendář není nakonfigurován. Kontaktujte správce.")
    
    context = {
        'events': events,
        'calendar_settings': calendar_settings,
        'error_message': error_message,
        'today': timezone.now().date(),
    }
    
    return render(request, 'football/google_calendar.html', context)
