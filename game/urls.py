from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('play/', views.play, name='play'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('history/', views.history, name='history'),
    path('result/', views.result, name='result'),
    path('settings/', views.profile_settings, name='profile_settings'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('manage-artworks/', views.manage_artworks, name='manage_artworks'),
    path('art-info/', views.art_info, name='art_info'),
]