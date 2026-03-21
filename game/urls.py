from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path(r'login/$', views.login, name='login'),
    path(r'^logout/$', views.logout, name='logout'), 
    path(r'^register/$', views.register, name='register'), 


    path(r'play/$', views.play, name='play'), 
    path(r'^result/', views.result, name='result'), 
    path(r'make_guess/', views.make_guess, name='make_guess'),
    path(r'leaderboard/$', views.leaderboard, name='leaderboard'), 


    path(r'history/$', views.history, name='history'), 
    path(r'settings/$', views.settings, name='settings'), 

    path(r'manage_users/', views.manage_users, name='manage_users'),
    path(r'manage_artworks/', views.manage_artworks, name='manage_artworks'),

    path(r'enable_user/', views.enable_user, name='enable_user'),
    path(r'disable_user/', views.disable_user, name='disable_user'),

    path('manage-users/enable/<int:user_id>/', views.enable_user, name='enable_user'),
    path('manage-users/disable/<int:user_id>/', views.disable_user, name='disable_user'),

    path(r'artwork_information/', views.artwork_information, name='artwork_information'),

]