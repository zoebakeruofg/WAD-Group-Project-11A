from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path(r'login/$', views.login, name='login'),
    path(r'^register/$', views.register, name='register'),
    path(r'^logout/$', views.logout, name='logout'),


    path(r'play/$', views.play, name='play'),
    path(r'^result/$', views.result, name='result'),
    path(r'^artwork/$', views.artwork, name='artwork'),


    path(r'leaderboard/$', views.leaderboard, name='leaderboard'),


    path(r'history/$', views.history, name='history'),
    path(r'settings/$', views.settings, name='settings'),
]