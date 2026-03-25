from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    path('play/', views.play, name='play'),
    path('result/', views.result, name='result'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('history/', views.history, name='history'),
    path('settings/', views.profile_settings, name='profile_settings'),

    path('manage-users/', views.manage_users, name='manage_users'),
    path('manage-artworks/', views.manage_artworks, name='manage_artworks'),

    path('manage-users/enable/<int:user_id>/', views.enable_user, name='enable_user'),
    path('manage-users/disable/<int:user_id>/', views.disable_user, name='disable_user'),

    path('manage-artworks/add/', views.add_artwork, name='add_artwork'),
    path('manage-artworks/edit/<int:artwork_id>/', views.edit_artwork, name='edit_artwork'),
    path('manage-artworks/delete/<int:artwork_id>/', views.delete_artwork, name='delete_artwork'),

    path('art-info/', views.art_info, name='art_info'),
    path('submit-guess/', views.submit_guess, name='submit_guess'),
]