from django.shortcuts import render
from django.http import HttpResponse
from .models import Artwork, Artist, Country
from .models import Artwork, GameSession, AdminProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.views.decorators.http import require_POST


def home(request):
    request.session.set_test_cookie()
    return render(request, "game/home.html", context)





def login(request):
    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        authority_type = request.POST.get("role", "user").strip().lower()

        matriculation_num = request.POST.get("guid", "").strip().upper()


    return render(request, "game/login.html")


def logout(request):
    logout(request)
    return redirect("home")


ADMIN_NUMS = {"3010809L", "3075329W", "3012337L", "2961000A", "2975768B",}

def register(request):

    if request.method == "POST":

        email = request.POST.get("email", "").strip()

        username = request.POST.get("username", "").strip()

        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        
        acc_type = request.POST.get("acc_type", "user").strip().lower()
        matriculation_num = request.POST.get("guid", "").strip().upper()

    if not email or not username or not password or not confirm_password:
        return render(
            request, 
            "game/create_account.html", 
            {"error": "Form error: ensure that all fields have been filled in"})

    if password != confirm_password:
        return render(
            request, 
            "game/create_account.html", 
            {"error": "Password error: passwords do not match"})

    if User.objects.filter(username=username).exists():
        return render(request,
        "game/create_account.html",
        {"error": "This username has already been taken, please try another one."})

    if User.objects.filter(email=email).exists():
        return render(request, "game/create_account.html", {"error": "An account with this email already exists, please go to login"})

    user_is_admin = False
    if acc_type == "admin":
        user_is_admin = True
        if matriculation_num not in ADMIN_NUMS:
            return render(request, "game/create_account.html", {"error" :"matriculation number invalid, only authenticated GUIDs can create an admin account"})
        
    user = User.objects.create_user(username=username, email=email, password=password)

    if user_is_admin:
        user.is_staff = True
        user.save()
        
        AdminProfile.objects.create(
            user=user,
            guid=guid
        )

    login(request, user)
    return redirect("home")

    return render(request, "game/create_account.html")





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

    continent_guess = request.POST.get("continent", "").strip().lower()
    country_guess = request.POST.get("country", "").strip().lower()

    artist_guess = request.POST.get("artist", "").strip().lower()

    year_guess = request.POST.get("year", "").strip().lower()


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




@staff_member_required(login_url='login')
def manage_users(request):
    return render(request, "game/manage_users.html")

@staff_member_required(login_url='login')
def manage_artworks(request):
    return render(request, "game/manage_artworks.html")




@staff_member_required(login_url='login')
def enable_user(request):
    return render(request)

@staff_member_required(login_url='login')
def disable_user(request):
    return render(request)




def artwork_information(request):
    return render(request, "game/art_info.html")