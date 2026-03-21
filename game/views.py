from django.shortcuts import render
from django.http import HttpResponse
from .models import Artwork, Artist, Country
from .models import Artwork, GameSession, AdminProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
import random
from django.db.models import Avg


def home(request):
    return render(request, "game/home.html", context)



#user authentication
def login(request):
    return render(request, "game/login.html")


def logout(request):
    logout(request)
    return redirect("home")


def register(request):
    login(request, user)
    return redirect("home")
    return render(request, "game/create_account.html")





@login_required(login_url='login')
def play(request):

    artworks_available = Artwork.objects.all()
    if not artworks_available:
        return JsonResponse({"success": False, "error": "No artwork available to play game"})

    artwork = random.choice(artworks_available)
    request.session["artwork_id"] = artwork.id

    return render(request, "game/play.html", {"artwork": artwork})


@login_required(login_url='login')
def result(request):
    result_data = request.session.get("last_result")
    return render(request, "game/result.html", {"result_data": result_data})


@login_required(login_url='login')
def make_guess(request):

    artwork_id = request.session.get("artwork_id")

    if not artwork_id:
        return JsonResponse({"success": False, "error": "No artwork available"})
    
    artwork = get_object_or_404(Artwork, id=artwork_id)

    continent_guess = request.POST.get("continent", "").strip().lower()
    region_guess = request.POST.get("region", "").strip().lower()
    country_guess = request.POST.get("country", "").strip().lower()

    artist_guess = request.POST.get("artist", "").strip().lower()

    year_guess = request.POST.get("year", "").strip()

    continent_answer = artwork.country.region.continent.name
    region_answer = artwork.country.region.name
    country_answer = artwork.country.name
    artist_answer = artwork.artist.name
    year_answer = artwork.year

    score = 0

    if continent_guess == continent_answer.lower():
        score += 20
        if region_guess == region_answer.lower():
            score += 20
            if country_guess == country_answer.lower():
                score += 20
    if artist_guess == artist_answer.lower():
        score += 20
    if str(year_guess) == str(year_answer):
        score += 20

    GameSession.objects.create(
        user=request.user,
        artwork=artwork,

        guess_continent=continent_guess,
        guess_country=country_guess,

        guess_artist=artist_guess,

        guess_year=year_guess if year_guess.isdigit() else None,

        score=score)

    result_data = {
    "score": score,
    "guesses": {
        "continent": continent_guess,
        "region": region_guess,
        "country": country_guess,

        "artist": artist_guess,

        "year": year_guess,
    },
    "correct_answers": {
        "continent": continent_answer,
        "region": region_answer,
        "country": country_answer,

        "artist": artist_answer,

        "year": year_answer,
    }}

    last_artwork_info = {
        "title": artwork.title,
        "image_url": artwork.image_url,
        "artist": artwork.artist.name,

        "country": artwork.country.name,
        "continent": artwork.country.region.continent.name,

        "year": artwork.year,
    }

    request.session["last_result"] = result_data
    request.session["last_artwork"] = last_artwork_info

    return JsonResponse({
        "success": True,
        "score": score, 
        "guesses": {
            "continent": continent_guess,
            "region" : region_guess,
            "country": country_guess,
            "artist": artist_guess,
            "year": year_guess,
        },
        "correct_answers": {
            "continent": continent_answer,
            "region" : region_answer,
            "country": country_answer,
            "artist": artist_answer,
            "year": year_answer,
        },
        "artwork_info": {
            "title": artwork.title,
            "artist": artwork.artist.name,
            "country": artwork.country.name,
            "continent": artwork.country.region.continent.name,
            "year": artwork.year,
            "image_url": artwork.image_url,
        }
    })

@login_required(login_url='login')
def leaderboard(request):

    leaderboard_data = (
        GameSession.objects
        .values("user__username")
        .annotate(avg_score=Avg("score"))
        .order_by("-avg_score")
    )

    leaderboard_row_data = [
        {"username": row["user__username"],
        "avg_score": round(row["avg_score"], 1)}
    ]
    
    for row in leaderboard_rows:
        return render(request, "game/leaderboard.html", {"leaderboard_row_data": leaderboard_row_data})



@login_required(login_url='login')
def history(request):
    return render(request, "game/history.html")


@login_required
def settings(request):
    email = request.POST.get("email", "").strip().lower()
    username = request.POST.get("username", "").strip().lower()
    password = request.POST.get("password", "").strip().lower()
    change_value = request.POST.get("settings-change-btn", "").strip().lower()

    #password change - fix later
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)


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
    artwork_info = request.session.get("last_artwork_info")
    return render(request, "game/art_info.html", {"artwork_info": artwork_info})