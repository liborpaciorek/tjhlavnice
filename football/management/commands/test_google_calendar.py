from django.core.management.base import BaseCommand
from football.models import GoogleCalendarSettings
import requests


class Command(BaseCommand):
    help = 'Test Google Calendar API connection and diagnose issues'

    def handle(self, *args, **options):
        try:
            settings = GoogleCalendarSettings.objects.first()
            if not settings:
                self.stdout.write(
                    self.style.ERROR('Google Calendar settings not found. Run: python manage.py setup_google_calendar')
                )
                return

            self.stdout.write(f"Testing Google Calendar API connection...")
            self.stdout.write(f"Calendar Name: {settings.name}")
            self.stdout.write(f"Calendar ID: {settings.calendar_id}")
            self.stdout.write(f"API Key: {'*' * (len(settings.api_key) - 8) + settings.api_key[-8:] if len(settings.api_key) > 8 else 'SHORT_KEY'}")
            self.stdout.write(f"Is Active: {settings.is_active}")
            
            if not settings.calendar_id:
                self.stdout.write(self.style.ERROR('Calendar ID is missing!'))
                return
                
            if not settings.api_key:
                self.stdout.write(self.style.ERROR('API Key is missing!'))
                return

            # Test the API connection
            url = f'https://www.googleapis.com/calendar/v3/calendars/{settings.calendar_id}/events'
            params = {
                'key': settings.api_key,
                'maxResults': 1,
                'singleEvents': 'true',
                'orderBy': 'startTime'
            }

            # Add headers to avoid referrer blocking
            headers = {
                'User-Agent': 'TJ-Hlavnice-Website/1.0',
                'Referer': 'https://tjhlavnice.cz/'
            }

            self.stdout.write("\nTesting API connection...")
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                events_count = len(data.get('items', []))
                self.stdout.write(
                    self.style.SUCCESS(f'✅ API connection successful! Found {events_count} events.')
                )
                
                # Show first event details if available
                if events_count > 0:
                    first_event = data['items'][0]
                    self.stdout.write(f"First event: {first_event.get('summary', 'No title')}")
                    
            elif response.status_code == 403:
                try:
                    error_data = response.json()
                    error_message = error_data.get('error', {}).get('message', 'Unknown error')
                    
                    self.stdout.write(self.style.ERROR(f'❌ 403 Forbidden Error: {error_message}'))
                    self.stdout.write("\nPossible causes:")
                    self.stdout.write("1. Invalid API Key")
                    self.stdout.write("2. API Key doesn't have Calendar API enabled")
                    self.stdout.write("3. Calendar is not public")
                    self.stdout.write("4. API Key has IP restrictions that don't include your server")
                    self.stdout.write("5. Daily quota exceeded")
                    
                    self.stdout.write("\nSolutions to try:")
                    self.stdout.write("1. Verify API Key in Google Cloud Console")
                    self.stdout.write("2. Enable Calendar API in Google Cloud Console")
                    self.stdout.write("3. Make sure calendar is public (in Google Calendar settings)")
                    self.stdout.write("4. Check API Key restrictions")
                    self.stdout.write("5. Wait if quota is exceeded (resets daily)")
                    
                except:
                    self.stdout.write(self.style.ERROR('❌ 403 Forbidden - Unable to parse error details'))
                    
            elif response.status_code == 404:
                self.stdout.write(self.style.ERROR('❌ 404 Not Found - Calendar ID is incorrect or calendar doesn\'t exist'))
                
            elif response.status_code == 400:
                try:
                    error_data = response.json()
                    error_message = error_data.get('error', {}).get('message', 'Unknown error')
                    self.stdout.write(self.style.ERROR(f'❌ 400 Bad Request: {error_message}'))
                except:
                    self.stdout.write(self.style.ERROR('❌ 400 Bad Request - Invalid request format'))
                    
            else:
                self.stdout.write(self.style.ERROR(f'❌ HTTP {response.status_code}: {response.text}'))

            # Show test URL for manual testing
            test_url = f"{url}?key={settings.api_key}&maxResults=1"
            self.stdout.write(f"\nManual test URL (open in browser):")
            self.stdout.write(f"{test_url}")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error during testing: {str(e)}'))
            
        self.stdout.write("\n" + "="*50)
        self.stdout.write("Google Calendar API Troubleshooting Guide:")
        self.stdout.write("="*50)
        self.stdout.write("1. Ensure calendar is PUBLIC in Google Calendar settings")
        self.stdout.write("2. Verify Calendar API is ENABLED in Google Cloud Console")
        self.stdout.write("3. Check API Key is correct and unrestricted (or allows your server IP)")
        self.stdout.write("4. Confirm Calendar ID format: something@group.calendar.google.com")
        self.stdout.write("5. Test manually by opening the test URL above in browser")
