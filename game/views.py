from django.shortcuts import render
from django.http import HttpResponse
from .models import Continent

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def home(request):

    context = {}

    request.session.set_test_cookie()



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

    if request.method == 'POST':
        continent_guess = ContinentForm(data=request.POST)


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
