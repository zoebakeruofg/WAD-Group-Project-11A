from django.shortcuts import render

# Create your views here.

def home(request):

    context = {}

    return render(request, "game/home.html", context)

def play(request):

    context = {}

    return render(request, "game/play.html", context)

def leaderboard(request):

    context = {}

    return render(request, "game/leaderboard.html", context)

def history(request):

    context = {}

    return render(request, "game/history.html", context)

def result(request):

    context = {}

    return render(request, "game/result.html", context)
