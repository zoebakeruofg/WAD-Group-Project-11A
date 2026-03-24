from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('play/', views.play, name='play'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('history/', views.history, name='history'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

]