from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from PIL import Image
import os
from django_ckeditor_5.fields import CKEditor5Field

class ClubInfo(models.Model):
    name = models.CharField(max_length=100, default="TJ Družba Hlavnice", verbose_name=_("Název klubu"))
    founded_year = models.IntegerField(default=1952, verbose_name=_("Rok založení"))
    history = CKEditor5Field(config_name='extends', blank=True, verbose_name=_("Historie klubu"), help_text=_("Historie a informace o klubu"))
    logo = models.ImageField(upload_to='club/', blank=True, null=True, verbose_name=_("Logo"))
    address = models.TextField(blank=True, verbose_name=_("Adresa"))
    contact_email = models.EmailField(blank=True, verbose_name=_("Kontaktní email"))
    contact_phone = models.CharField(max_length=20, blank=True, verbose_name=_("Kontaktní telefon"))
    
    class Meta:
        verbose_name = _("Informace o klubu")
        verbose_name_plural = _("Informace o klubu")
    
    def __str__(self):
        return self.name

class League(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Název soutěže"))
    season = models.CharField(max_length=20, verbose_name=_("Sezóna"))
    description = models.TextField(blank=True, verbose_name=_("Popis"))
    
    class Meta:
        unique_together = ['name', 'season']
        verbose_name = _("Soutěž")
        verbose_name_plural = _("Soutěže")
    
    def __str__(self):
        return f"{self.name} - {self.season}"

class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Název týmu"))
    flag = models.ImageField(upload_to='teams/', blank=True, null=True, verbose_name=_("Vlajka/Logo"))
    founded = models.IntegerField(blank=True, null=True, verbose_name=_("Rok založení"))
    city = models.CharField(max_length=100, blank=True, verbose_name=_("Město"))
    league = models.ForeignKey(League, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_("Soutěž"))
    is_club_team = models.BooleanField(default=False, verbose_name=_("Náš tým"), help_text=_("Označte, pokud je to tým TJ Hlavnice"))
    
    class Meta:
        verbose_name = _("Tým")
        verbose_name_plural = _("Týmy")
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.flag:
            img = Image.open(self.flag.path)
            if img.height > 100 or img.width > 100:
                img.thumbnail((100, 100))
                img.save(self.flag.path)

class Player(models.Model):
    POSITION_CHOICES = [
        ('GK', _('Brankář')),
        ('DEF', _('Obránce')),
        ('MID', _('Záložník')),
        ('FWD', _('Útočník')),
    ]
    
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players', verbose_name=_("Tým"))
    jersey_number = models.IntegerField(verbose_name=_("Číslo dresu"))
    first_name = models.CharField(max_length=50, verbose_name=_("Křestní jméno"))
    last_name = models.CharField(max_length=50, verbose_name=_("Příjmení"))
    position = models.CharField(max_length=3, choices=POSITION_CHOICES, verbose_name=_("Pozice"))
    birth_date = models.DateField(blank=True, null=True, verbose_name=_("Datum narození"))
    photo = models.ImageField(upload_to='players/', blank=True, null=True, verbose_name=_("Fotografie"))
    goals = models.IntegerField(default=0, verbose_name=_("Góly"))
    yellow_cards = models.IntegerField(default=0, verbose_name=_("Žluté karty"))
    red_cards = models.IntegerField(default=0, verbose_name=_("Červené karty"))
    
    class Meta:
        unique_together = ['team', 'jersey_number']
        ordering = ['jersey_number']
        verbose_name = _("Hráč")
        verbose_name_plural = _("Hráči")
    
    def __str__(self):
        return f"{self.jersey_number}. {self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo.path)
            if img.height > 300 or img.width > 300:
                img.thumbnail((300, 300))
                img.save(self.photo.path)

class Management(models.Model):
    ROLE_CHOICES = [
        ('PRESIDENT', _('Předseda')),
        ('COACH', _('Trenér')),
        ('ASSISTANT', _('Asistent trenéra')),
        ('TREASURER', _('Pokladník')),
        ('SECRETARY', _('Sekretář')),
        ('MANAGER', _('Manažer')),
        ('OTHER', _('Ostatní')),
    ]
    
    first_name = models.CharField(max_length=50, verbose_name=_("Křestní jméno"))
    last_name = models.CharField(max_length=50, verbose_name=_("Příjmení"))
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name=_("Funkce"))
    photo = models.ImageField(upload_to='management/', blank=True, null=True, verbose_name=_("Fotografie"))
    bio = CKEditor5Field(config_name='extends', blank=True, verbose_name=_("Biografie"), help_text=_("Biografie a informace"))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Telefon"))
    email = models.EmailField(blank=True, verbose_name=_("Email"))
    order = models.IntegerField(default=0, verbose_name=_("Pořadí"), help_text=_("Pořadí zobrazení"))
    
    class Meta:
        ordering = ['order', 'role']
        verbose_name = _("Vedení klubu")
        verbose_name_plural = _("Vedení klubu")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_role_display()}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo.path)
            if img.height > 300 or img.width > 300:
                img.thumbnail((300, 300))
                img.save(self.photo.path)

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Nadpis"))
    content = CKEditor5Field(config_name='extends', verbose_name=_("Obsah"), help_text=_("Obsah článku"))
    image = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name=_("Obrázek"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Vytvořeno"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Upraveno"))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Autor"))
    is_featured = models.BooleanField(default=False, verbose_name=_("Doporučený článek"))
    published = models.BooleanField(default=True, verbose_name=_("Publikováno"))
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Aktualita")
        verbose_name_plural = _("Aktuality")
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'pk': self.pk})
    
    def get_image_url(self):
        """Safely get image URL or return None if image doesn't exist"""
        try:
            if self.image and hasattr(self.image, 'url'):
                return self.image.url
        except (ValueError, AttributeError):
            pass
        return None
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            try:
                img = Image.open(self.image.path)
                if img.height > 800 or img.width > 800:
                    img.thumbnail((800, 800))
                    img.save(self.image.path)
            except (FileNotFoundError, OSError, AttributeError):
                pass

class Match(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches', verbose_name=_("Domácí tým"))
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches', verbose_name=_("Hostující tým"))
    date = models.DateTimeField(verbose_name=_("Datum a čas"))
    league = models.ForeignKey(League, on_delete=models.CASCADE, verbose_name=_("Soutěž"))
    home_score = models.IntegerField(blank=True, null=True, verbose_name=_("Skóre domácích"))
    away_score = models.IntegerField(blank=True, null=True, verbose_name=_("Skóre hostů"))
    location = models.CharField(max_length=100, blank=True, verbose_name=_("Místo konání"))
    referee = models.CharField(max_length=100, blank=True, verbose_name=_("Rozhodčí"))
    notes = models.TextField(blank=True, verbose_name=_("Poznámky"))
    
    class Meta:
        ordering = ['-date']
        verbose_name = _("Zápas")
        verbose_name_plural = _("Zápasy")
    
    def __str__(self):
        if self.home_score is not None and self.away_score is not None:
            return f"{self.home_team} {self.home_score}:{self.away_score} {self.away_team}"
        return f"{self.home_team} vs {self.away_team}"
    
    @property
    def is_finished(self):
        return self.home_score is not None and self.away_score is not None
    
    @property
    def is_club_match(self):
        return self.home_team.is_club_team or self.away_team.is_club_team

class Standing(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name=_("Tým"))
    league = models.ForeignKey(League, on_delete=models.CASCADE, verbose_name=_("Soutěž"))
    position = models.IntegerField(verbose_name=_("Pozice"))
    played = models.IntegerField(default=0, verbose_name=_("Odehráno"))
    won = models.IntegerField(default=0, verbose_name=_("Výhry"))
    drawn = models.IntegerField(default=0, verbose_name=_("Remízy"))
    lost = models.IntegerField(default=0, verbose_name=_("Prohry"))
    goals_for = models.IntegerField(default=0, verbose_name=_("Góly vstřelené"))
    goals_against = models.IntegerField(default=0, verbose_name=_("Góly obdržené"))
    points = models.IntegerField(default=0, verbose_name=_("Body"))
    
    class Meta:
        unique_together = ['team', 'league']
        ordering = ['position']
        verbose_name = _("Tabulka")
        verbose_name_plural = _("Tabulky")
    
    def __str__(self):
        return f"{self.position}. {self.team.name} - {self.points} pts"
    
    @property
    def goal_difference(self):
        return self.goals_for - self.goals_against

class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Název události"))
    description = models.TextField(blank=True, verbose_name=_("Popis"))
    date = models.DateTimeField(verbose_name=_("Datum a čas"))
    location = models.CharField(max_length=100, blank=True, verbose_name=_("Místo konání"))
    is_match = models.BooleanField(default=False, verbose_name=_("Je to zápas"))
    match = models.ForeignKey(Match, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_("Zápas"))
    
    class Meta:
        ordering = ['date']
        verbose_name = _("Událost")
        verbose_name_plural = _("Události")
    
    def __str__(self):
        return f"{self.title} - {self.date.strftime('%Y-%m-%d')}"

class Gallery(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Název"))
    description = models.TextField(blank=True, verbose_name=_("Popis"))
    image = models.ImageField(upload_to='gallery/', verbose_name=_("Obrázek"))
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Nahráno"))
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_("Událost"))
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = _("Galerie")
        verbose_name_plural = _("Galerie")
    
    def __str__(self):
        return self.title
    
    def get_image_url(self):
        """Safely get image URL or return None if image doesn't exist"""
        try:
            if self.image and hasattr(self.image, 'url'):
                return self.image.url
        except (ValueError, AttributeError):
            pass
        return None
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            try:
                img = Image.open(self.image.path)
                if img.height > 1200 or img.width > 1200:
                    img.thumbnail((1200, 1200))
                    img.save(self.image.path)
            except (FileNotFoundError, OSError, AttributeError):
                pass

class PageVisit(models.Model):
    page_name = models.CharField(max_length=100, verbose_name=_("Název stránky"))
    ip_address = models.GenericIPAddressField(verbose_name=_("IP adresa"))
    user_agent = models.TextField(verbose_name=_("User Agent"))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("Čas návštěvy"))
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = _("Návštěva stránky")
        verbose_name_plural = _("Návštěvy stránek")
    
    def __str__(self):
        return f"{self.page_name} - {self.timestamp}"

class MainPage(models.Model):
    """Single model instance to control main page content"""
    featured_news = models.ManyToManyField(News, blank=True, verbose_name=_("Doporučené aktuality"), limit_choices_to={'published': True})
    
    class Meta:
        verbose_name = _("Konfigurace hlavní stránky")
        verbose_name_plural = _("Konfigurace hlavní stránky")
    
    def __str__(self):
        return "Main Page Settings"
    
    def get_latest_news(self):
        return News.objects.filter(published=True)[:3]
    
    def get_upcoming_match(self):
        from django.utils import timezone
        return Match.objects.filter(
            date__gte=timezone.now(),
            home_team__is_club_team=True
        ).first() or Match.objects.filter(
            date__gte=timezone.now(),
            away_team__is_club_team=True
        ).first()
    
    def get_recent_matches(self):
        from django.utils import timezone
        return Match.objects.filter(
            date__lt=timezone.now(),
            home_score__isnull=False,
            away_score__isnull=False
        ).filter(
            models.Q(home_team__is_club_team=True) | models.Q(away_team__is_club_team=True)
        )[:2]
    
    def get_club_standing(self):
        club_team = Team.objects.filter(is_club_team=True).first()
        if club_team:
            try:
                standing = Standing.objects.get(team=club_team)
                # Get surrounding teams (2 above, club team, 2 below)
                position = standing.position
                return Standing.objects.filter(
                    league=standing.league,
                    position__gte=max(1, position-2),
                    position__lte=position+2
                ).order_by('position')
            except Standing.DoesNotExist:
                return Standing.objects.none()
        return Standing.objects.none()
