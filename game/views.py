from django.shortcuts import render
from django.http import HttpResponse
from .models import Continent

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val





def home(request):
    request.session.set_test_cookie()
    return render(request, "game/home.html", context)





def login(request):
    return render(request, "game/login.html")


def logout(request):
    logout(request)
    return redirect("home")


def register(request):
    return render(request, "game/register.html")





@login_required(login_url='login')
def play(request):

    if request.method == 'POST':
        continent_guess = ContinentForm(data=request.POST)

    return render(request, "game/play.html")


@login_required(login_url='login')
def result(request):
    result_data = request.session.get("last_result")
    return render(request, "game/result.html", {"result_data": result_data})


@login_required(login_url='login')
def make_guess(request):
    return render(request, "game/artwork_information.html")

@login_required(login_url='login')
def leaderboard(request):
    return render(request, "game/leaderboard.html")





@login_required(login_url='login')
def history(request):
    return render(request, "game/history.html")


@login_required
def settings(request):
    return render(request, "game/settings.html")





def manage_users(request):
    return render(request, "game/manage_users.html")


def manage_artworks(request):
    return render(request, "game/manage_artworks.html")





def enable_user(request):
    return render(request)


def disable_user(request):
    return render(request)




def artwork_information(request):
    return render(request, "game/art_info.html")