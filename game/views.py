from django.shortcuts import render, redirect
from django.contrib.auth import logout


def home(request):
    return render(request, "game/home.html")


def play(request):
    return render(request, "game/play.html")


def leaderboard(request):
    return render(request, "game/leaderboard.html")


def history(request):
    return render(request, "game/history.html")


def result(request):
    return render(request, "game/result.html")


def profile_settings(request):
    return render(request, "game/profile_settings.html")


def register(request):
    return render(request, "game/create_account.html")


def login_view(request):
    return render(request, "game/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


def admin_dashboard(request):
    return render(request, "game/admin_dashboard.html")


def manage_users(request):
    return render(request, "game/manage_users.html")


def manage_artworks(request):
    return render(request, "game/manage_artworks.html")

def art_info(request):
    return render(request, "game/art_info.html")