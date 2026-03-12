from django.shortcuts import render
from django.http import HttpResponse


def home(request):

    context = {}

    return render(request, "game/home.html", context)




def login(request):

    context = {}

    return render(request, "game/login.html", context)


def register(request):

    context = {}

    return render(request, "game/register.html", context)


@login_required
def logout(request):

    context = {}

    return render(request, "game/logout.html", context)




@login_required
def play(request):

    context = {}

    return render(request, "game/play.html", context)

@login_required
def result(request):

    context = {}

    return render(request, "game/result.html", context)

def artwork(request):

    context = {}

    return render(request, "game/artwork.html", context)




def leaderboard(request):

    context = {}

    return render(request, "game/leaderboard.html", context)

@login_required
def history(request):

    context = {}

    return render(request, "game/history.html", context)


@login_required
def settings(request):

    context = {}

    return render(request, "game/settings.html", context)
