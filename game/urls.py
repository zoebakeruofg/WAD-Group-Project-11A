from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'), 
    path('register/', views.register, name='register'), 


    path('play/', views.play, name='play'), 
    path('result/', views.result, name='result'), 
    path('make_guess/', views.make_guess, name='make_guess'),
    path('leaderboard/', views.leaderboard, name='leaderboard'), 


    path('history/', views.history, name='history'), 
    path('settings/', views.settings, name='settings'), 

    path('manage_users/', views.manage_users, name='manage_users'),
    path('manage_artworks/', views.manage_artworks, name='manage_artworks'),

    path('enable_user/', views.enable_user, name='enable_user'),
    path('disable_user/', views.disable_user, name='disable_user'),

    path('manage_users/enable/<int:user_id>/', views.enable_user, name='enable_user'),
    path('manage_users/disable/<int:user_id>/', views.disable_user, name='disable_user'),

    path('manage_artworks/add/', views.add_artwork, name='add_artwork'),
    path('manage_artworks/edit/<int:artwork_id>/', views.edit_artwork, name='edit_artwork'),
    path('manage_artworks/delete/<int:artwork_id>/', views.delete_artwork, name='delete_artwork'),

    path('artwork_information/', views.artwork_information, name='artwork_information'),
]