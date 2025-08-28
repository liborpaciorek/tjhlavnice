from django.core.management.base import BaseCommand
from football.models import GoogleCalendarSettings


class Command(BaseCommand):
    help = 'Creates Google Calendar settings if none exist'

    def handle(self, *args, **options):
        # Check if settings already exist
        if GoogleCalendarSettings.objects.exists():
            self.stdout.write(
                self.style.WARNING('Google Calendar settings already exist.')
            )
            settings = GoogleCalendarSettings.objects.first()
            self.stdout.write(f"Current settings: {settings.name}")
            self.stdout.write(f"Status: {'Active' if settings.is_active else 'Inactive'}")
        else:
            # Create default settings
            settings = GoogleCalendarSettings.objects.create(
                name="Kalendář TJ Družba Hlavnice",
                is_active=False,  # Inactive by default until configured
                max_events=50,
                show_past_events=True,
                past_events_days=30
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created Google Calendar settings: {settings.name}'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    'Please configure the Calendar ID and API key in Django admin panel.'
                )
            )
