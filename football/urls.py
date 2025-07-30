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
    path('gallery/', views.GalleryListView.as_view(), name='gallery'),
    path('club/', views.club_info, name='club_info'),
    path('zasady-ochrany-osobnich-udaju/', views.privacy_policy, name='privacy_policy'),
]
