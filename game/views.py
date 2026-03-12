from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):

    context = {}

    return render(request, "game/home.html", context)




def login(request):

    context = {}

    return render(request, "game/login.html", context)


def register(request):

    context = {}

    return render(request, "game/register.html", context)


def logout(request):

    context = {}

    return render(request, "game/logout.html", context)





def play(request):

    context = {}

    return render(request, "game/play.html", context)

def result(request):

    context = {}

    return render(request, "game/result.html", context)

def artwork(request):

    context = {}

    return render(request, "game/artwork.html", context)


    

def leaderboard(request):

    context = {}

    return render(request, "game/leaderboard.html", context)

def history(request):

    context = {}

    return render(request, "game/history.html", context)
