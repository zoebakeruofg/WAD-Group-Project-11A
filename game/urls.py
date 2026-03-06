from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('play/', views.play, name='play'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('history/', views.history, name='history'),
    path('result/', views.result, name='result'),
]