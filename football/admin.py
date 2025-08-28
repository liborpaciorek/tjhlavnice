from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from .models import (
    ClubInfo, League, Team, Player, Management, News, 
    Match, Standing, Event, Gallery, GalleryAlbum, PageVisit, MainPage, GoogleCalendarSettings, BulkImageUpload
)
from .forms import BulkImageUploadForm

@admin.register(ClubInfo)
class ClubInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'founded_year']
    fields = ['name', 'founded_year', 'history', 'logo', 'address', 'contact_email', 'contact_phone']
    
    class Media:
        css = {
            'all': ('admin/css/widgets.css', 'css/custom.css',),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Czech admin interface customization
        self.verbose_name = _('Informace o klubu')
        self.verbose_name_plural = _('Informace o klubu')

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ['name', 'season']
    list_filter = ['season']
    search_fields = ['name']

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'city', 'league', 'is_club_team', 'flag_preview']
    list_filter = ['league', 'is_club_team', 'city']
    search_fields = ['name', 'short_name', 'city']
    fields = ['name', 'short_name', 'flag', 'founded', 'city', 'league', 'is_club_team']
    
    def flag_preview(self, obj):
        if obj.flag:
            return format_html('<img src="{}" width="30" height="20" />', obj.flag.url)
        return _("Bez vlajky")
    flag_preview.short_description = _("Vlajka")

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
        return _("Bez fotografie")
    photo_preview.short_description = _("Fotografie")

@admin.register(Management)
class ManagementAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'role', 'phone', 'email', 'order', 'photo_preview']
    list_filter = ['role']
    search_fields = ['first_name', 'last_name']
    ordering = ['order', 'role']
    fields = ['first_name', 'last_name', 'role', 'photo', 'bio', 'phone', 'email', 'order']
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="40" height="40" style="border-radius: 50%;" />', obj.photo.url)
        return _("Bez fotografie")
    photo_preview.short_description = _("Fotografie")
    
    class Media:
        css = {
            'all': ('admin/css/widgets.css', 'css/custom.css',),
        }

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'published', 'is_featured', 'image_preview']
    list_filter = ['published', 'is_featured', 'created_at', 'author']
    search_fields = ['title', 'content']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    fields = ['title', 'content', 'image', 'author', 'published', 'is_featured']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="40" />', obj.image.url)
        return _("Bez obrázku")
    image_preview.short_description = _("Obrázek")
    
    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    class Media:
        css = {
            'all': ('admin/css/widgets.css', 'css/custom.css',),
        }

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['match_display', 'round_number', 'date', 'league', 'is_finished', 'is_club_match']
    list_filter = ['league', 'round_number', 'date', 'home_team__is_club_team', 'away_team__is_club_team']
    search_fields = ['home_team__name', 'away_team__name']
    date_hierarchy = 'date'
    ordering = ['-date']
    fields = ['home_team', 'away_team', 'date', 'league', 'round_number', 'home_score', 'away_score', 'location', 'referee', 'notes']
    
    def match_display(self, obj):
        if obj.is_finished:
            return f"{obj.home_team} {obj.home_score}:{obj.away_score} {obj.away_team}"
        return f"{obj.home_team} vs {obj.away_team}"
    match_display.short_description = _("Zápas")

@admin.register(Standing)
class StandingAdmin(admin.ModelAdmin):
    list_display = ['position', 'team', 'league', 'played', 'won', 'drawn', 'lost', 'goal_difference', 'points', 'highlight_club']
    list_filter = ['league']
    ordering = ['league', 'position']
    
    def highlight_club(self, obj):
        if obj.team.is_club_team:
            return format_html('<span style="color: red; font-weight: bold;">TJ Hlavnice</span>')
        return ""
    highlight_club.short_description = _("Náš tým")

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location', 'is_match']
    list_filter = ['is_match', 'date']
    search_fields = ['title', 'description']
    date_hierarchy = 'date'
    ordering = ['-date']

class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 1
    fields = ['title', 'image', 'description', 'uploaded_at']
    readonly_fields = ['uploaded_at']

@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'event', 'cover_preview', 'bulk_upload_link']
    list_filter = ['created_at', 'event']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    inlines = [GalleryInline]
    fields = ['title', 'description', 'event', 'cover_image']
    
    def cover_preview(self, obj):
        url = obj.get_cover_url()
        if url:
            return format_html('<img src="{}" width="80" height="60" />', url)
        return _("Bez obrázku")
    cover_preview.short_description = _("Titulka")
    
    def bulk_upload_link(self, obj):
        from django.urls import reverse
        url = reverse('admin:football_bulkimageupload_add') + f'?album={obj.pk}'
        return format_html(
            '<a href="{}" class="button" style="background: #007cba; color: white; padding: 5px 10px; '
            'text-decoration: none; border-radius: 3px; font-size: 11px;">'
            '<i class="fas fa-upload"></i> Hromadné nahrání'
            '</a>',
            url
        )
    bulk_upload_link.short_description = _("Akce")
    bulk_upload_link.allow_tags = True

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_at', 'album', 'event', 'image_preview']
    list_filter = ['uploaded_at', 'event', 'album']
    search_fields = ['title', 'description']
    date_hierarchy = 'uploaded_at'
    ordering = ['-uploaded_at']
    fields = ['title', 'description', 'image', 'album', 'event']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="60" />', obj.image.url)
        return _("Bez obrázku")
    image_preview.short_description = _("Obrázek")


@admin.register(BulkImageUpload)
class BulkImageUploadAdmin(admin.ModelAdmin):
    """Admin for bulk image upload"""
    form = BulkImageUploadForm
    list_display = ['album', 'event', 'uploaded_at', 'default_title_prefix']
    list_filter = ['uploaded_at', 'album', 'event']
    ordering = ['-uploaded_at']
    fields = ['album', 'event', 'default_title_prefix', 'images']
    
    def get_form(self, request, obj=None, **kwargs):
        """Pre-fill album field if passed in URL"""
        form = super().get_form(request, obj, **kwargs)
        
        # Pre-fill album from URL parameter
        album_id = request.GET.get('album')
        if album_id and not obj:
            try:
                album = GalleryAlbum.objects.get(pk=album_id)
                form.base_fields['album'].initial = album
                # Also set default title prefix based on album name
                form.base_fields['default_title_prefix'].initial = f"{album.title} -"
            except GalleryAlbum.DoesNotExist:
                pass
        
        return form
    
    def save_model(self, request, obj, form, change):
        """Override save to handle multiple images"""
        if not change:  # Only for new instances
            created_galleries = form.save(commit=True)
            if created_galleries:
                from django.contrib import messages
                count = len(created_galleries)
                messages.success(
                    request, 
                    f"Úspěšně nahráno {count} obrázků do galerie '{obj.album.title}'"
                )
        else:
            # For existing instances, just save normally (shouldn't happen much)
            super().save_model(request, obj, form, change)
    
    def response_add(self, request, obj, post_url_continue=None):
        """Redirect back to album admin after successful upload"""
        from django.contrib import admin
        from django.http import HttpResponseRedirect
        from django.urls import reverse
        
        # If we came from an album, redirect back to the album list
        if obj and obj.album:
            return HttpResponseRedirect(reverse('admin:football_galleryalbum_changelist'))
        
        return super().response_add(request, obj, post_url_continue)
    
    def has_change_permission(self, request, obj=None):
        """Disable editing of bulk uploads"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Allow deletion of bulk upload records"""
        return True
    
    class Media:
        css = {
            'all': ('admin/css/widgets.css', 'css/custom.css',),
        }
        js = ('admin/js/bulk_upload.js',)

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


@admin.register(GoogleCalendarSettings)
class GoogleCalendarSettingsAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'calendar_id', 'updated_at']
    fields = [
        'name', 
        'calendar_id', 
        'api_key', 
        'is_active', 
        'max_events', 
        'show_past_events', 
        'past_events_days'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not GoogleCalendarSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    class Media:
        css = {
            'all': ('admin/css/widgets.css', 'css/custom.css',),
        }

    
    class Media:
        css = {
            'all': ('admin/css/widgets.css', 'css/custom.css',),
        }
