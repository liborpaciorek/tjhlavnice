from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('team/', views.team_lineup, name='team_lineup'),
    path('management/', views.management, name='management'),
    path('matches/', views.MatchListView.as_view(), name='matches'),
    path('standings/', views.standings, name='standings'),
    path('calendar/', views.EventListView.as_view(), name='calendar'),
    path('kalendar/', views.google_calendar_view, name='google_calendar'),
    path('gallery/', views.GalleryAlbumListView.as_view(), name='gallery'),
    path('gallery/<int:pk>/', views.GalleryAlbumDetailView.as_view(), name='gallery_detail'),
    path('club/', views.club_info, name='club_info'),
]
