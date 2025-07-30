from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
import os

class ClubInfo(models.Model):
    name = models.CharField(max_length=100, default="TJ Družba Hlavnice")
    founded_year = models.IntegerField(default=1952)
    history = models.TextField(blank=True)
    logo = models.ImageField(upload_to='club/', blank=True, null=True)
    address = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    
    class Meta:
        verbose_name = "Club Information"
        verbose_name_plural = "Club Information"
    
    def __str__(self):
        return self.name

class League(models.Model):
    name = models.CharField(max_length=100)
    season = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['name', 'season']
    
    def __str__(self):
        return f"{self.name} - {self.season}"

class Team(models.Model):
    name = models.CharField(max_length=100)
    flag = models.ImageField(upload_to='teams/', blank=True, null=True)
    founded = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE, blank=True, null=True)
    is_club_team = models.BooleanField(default=False, help_text="Mark if this is TJ Hlavnice team")
    
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
        ('GK', 'Goalkeeper'),
        ('DEF', 'Defender'),
        ('MID', 'Midfielder'),
        ('FWD', 'Forward'),
    ]
    
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    jersey_number = models.IntegerField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=3, choices=POSITION_CHOICES)
    birth_date = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='players/', blank=True, null=True)
    goals = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['team', 'jersey_number']
        ordering = ['jersey_number']
    
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
        ('PRESIDENT', 'President'),
        ('COACH', 'Coach'),
        ('ASSISTANT', 'Assistant Coach'),
        ('TREASURER', 'Treasurer'),
        ('SECRETARY', 'Secretary'),
        ('MANAGER', 'Manager'),
        ('OTHER', 'Other'),
    ]
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    photo = models.ImageField(upload_to='management/', blank=True, null=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    order = models.IntegerField(default=0, help_text="Display order")
    
    class Meta:
        ordering = ['order', 'role']
    
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
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)
    published = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "News"
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 800 or img.width > 800:
                img.thumbnail((800, 800))
                img.save(self.image.path)

class Match(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    date = models.DateTimeField()
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    home_score = models.IntegerField(blank=True, null=True)
    away_score = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    referee = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-date']
    
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
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    position = models.IntegerField()
    played = models.IntegerField(default=0)
    won = models.IntegerField(default=0)
    drawn = models.IntegerField(default=0)
    lost = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['team', 'league']
        ordering = ['position']
    
    def __str__(self):
        return f"{self.position}. {self.team.name} - {self.points} pts"
    
    @property
    def goal_difference(self):
        return self.goals_for - self.goals_against

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateTimeField()
    location = models.CharField(max_length=100, blank=True)
    is_match = models.BooleanField(default=False)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        ordering = ['date']
    
    def __str__(self):
        return f"{self.title} - {self.date.strftime('%Y-%m-%d')}"

class Gallery(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name_plural = "Gallery"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 1200 or img.width > 1200:
                img.thumbnail((1200, 1200))
                img.save(self.image.path)

class PageVisit(models.Model):
    page_name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.page_name} - {self.timestamp}"

class MainPage(models.Model):
    """Single model instance to control main page content"""
    featured_news = models.ManyToManyField(News, blank=True, limit_choices_to={'published': True})
    
    class Meta:
        verbose_name = "Main Page Configuration"
        verbose_name_plural = "Main Page Configuration"
    
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
