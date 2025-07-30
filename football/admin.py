from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ClubInfo, League, Team, Player, Management, News, 
    Match, Standing, Event, Gallery, PageVisit, MainPage
)

@admin.register(ClubInfo)
class ClubInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'founded_year']
    fields = ['name', 'founded_year', 'history', 'logo', 'address', 'contact_email', 'contact_phone']

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ['name', 'season']
    list_filter = ['season']
    search_fields = ['name']

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'league', 'is_club_team', 'flag_preview']
    list_filter = ['league', 'is_club_team', 'city']
    search_fields = ['name', 'city']
    
    def flag_preview(self, obj):
        if obj.flag:
            return format_html('<img src="{}" width="30" height="20" />', obj.flag.url)
        return "No flag"
    flag_preview.short_description = "Flag"

class PlayerInline(admin.TabularInline):
    model = Player
    extra = 1
    fields = ['jersey_number', 'first_name', 'last_name', 'position', 'goals', 'yellow_cards', 'red_cards']

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['jersey_number', 'full_name', 'team', 'position', 'goals', 'photo_preview']
    list_filter = ['team', 'position']
    search_fields = ['first_name', 'last_name', 'team__name']
    ordering = ['team', 'jersey_number']
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="40" height="40" style="border-radius: 50%;" />', obj.photo.url)
        return "No photo"
    photo_preview.short_description = "Photo"

@admin.register(Management)
class ManagementAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'role', 'phone', 'email', 'order', 'photo_preview']
    list_filter = ['role']
    search_fields = ['first_name', 'last_name']
    ordering = ['order', 'role']
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="40" height="40" style="border-radius: 50%;" />', obj.photo.url)
        return "No photo"
    photo_preview.short_description = "Photo"

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'published', 'is_featured', 'image_preview']
    list_filter = ['published', 'is_featured', 'created_at', 'author']
    search_fields = ['title', 'content']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="40" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Image"

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['match_display', 'date', 'league', 'is_finished', 'is_club_match']
    list_filter = ['league', 'date', 'home_team__is_club_team', 'away_team__is_club_team']
    search_fields = ['home_team__name', 'away_team__name']
    date_hierarchy = 'date'
    ordering = ['-date']
    
    def match_display(self, obj):
        if obj.is_finished:
            return f"{obj.home_team} {obj.home_score}:{obj.away_score} {obj.away_team}"
        return f"{obj.home_team} vs {obj.away_team}"
    match_display.short_description = "Match"

@admin.register(Standing)
class StandingAdmin(admin.ModelAdmin):
    list_display = ['position', 'team', 'league', 'played', 'won', 'drawn', 'lost', 'goal_difference', 'points', 'highlight_club']
    list_filter = ['league']
    ordering = ['league', 'position']
    
    def highlight_club(self, obj):
        if obj.team.is_club_team:
            return format_html('<span style="color: red; font-weight: bold;">TJ Hlavnice</span>')
        return ""
    highlight_club.short_description = "Club Team"

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location', 'is_match']
    list_filter = ['is_match', 'date']
    search_fields = ['title', 'description']
    date_hierarchy = 'date'
    ordering = ['-date']

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_at', 'event', 'image_preview']
    list_filter = ['uploaded_at', 'event']
    search_fields = ['title', 'description']
    date_hierarchy = 'uploaded_at'
    ordering = ['-uploaded_at']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="60" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Image"

@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    list_display = ['page_name', 'ip_address', 'timestamp', 'short_user_agent']
    list_filter = ['page_name', 'timestamp']
    search_fields = ['page_name', 'ip_address']
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']
    readonly_fields = ['page_name', 'ip_address', 'user_agent', 'timestamp']
    
    def short_user_agent(self, obj):
        return obj.user_agent[:50] + "..." if len(obj.user_agent) > 50 else obj.user_agent
    short_user_agent.short_description = "User Agent"
    
    def has_add_permission(self, request):
        return False

@admin.register(MainPage)
class MainPageAdmin(admin.ModelAdmin):
    filter_horizontal = ['featured_news']
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not MainPage.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False
