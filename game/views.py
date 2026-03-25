from django.shortcuts import render, redirect
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
from django.http import HttpResponse, JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from .models import Artwork, Artist, Country, Continent, Region, GameSession, AdminProfile

ALLOWED_ADMIN_GUIDS = {
    "3010809L",
    "3075329W",
    "3012337L",
    "2961000A",
    "2975768B",
}

def home(request):
    context = {}
    return render(request, "game/home.html", context)


#user authentication
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        role = request.POST.get("role", "user").strip().lower()
        guid = request.POST.get("guid", "").strip().upper()

        existing_user = User.objects.filter(username=username).first()

        if existing_user and not existing_user.is_active:
            return render(request, "game/login.html", {
                "error": "Your account is disabled. Please contact an admin."
            })

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, "game/login.html", {
                "error": "Invalid username or password."
            })

        if user.is_staff:
            if role != "admin":
                return render(request, "game/login.html", {
                    "error": "This account must log in using the Admin option and the correct GUID."
                })

            if guid == "":
                return render(request, "game/login.html", {
                    "error": "GUID is required for admin login."
                })

            if guid not in ALLOWED_ADMIN_GUIDS:
                return render(request, "game/login.html", {
                    "error": "Invalid admin GUID."
                })

            try:
                admin_profile = user.admin_profile
            except AdminProfile.DoesNotExist:
                return render(request, "game/login.html", {
                    "error": "This admin account does not have a saved GUID."
                })

            if admin_profile.guid != guid:
                return render(request, "game/login.html", {
                    "error": "This GUID does not match this admin account."
                })

            login(request, user)
            return redirect("home")
        
        if role == "admin":
            return render(request, "game/login.html", {
                "error": "This account is not registered as an admin."
            })

        login(request, user)
        return redirect("home")

    return render(request, "game/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


def register(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        account_type = request.POST.get("account_type", "user").strip().lower()
        guid = request.POST.get("guid", "").strip().upper()

        if not email or not username or not password or not confirm_password:
            return render(request, "game/create_account.html", {
                "error": "Please fill in all fields."
            })

        if password != confirm_password:
            return render(request, "game/create_account.html", {
                "error": "Passwords do not match."
            })

        if User.objects.filter(username=username).exists():
            return render(request, "game/create_account.html", {
                "error": "Username already exists."
            })

        if User.objects.filter(email=email).exists():
            return render(request, "game/create_account.html", {
                "error": "Email already exists."
            })

        is_admin = False

        if account_type == "admin":
            if guid not in ALLOWED_ADMIN_GUIDS:
                return render(request, "game/create_account.html", {
                    "error": "This GUID is not allowed to create an admin account."
                })
            is_admin = True

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        if is_admin:
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

    artworks_available = Artwork.objects.all()
    if not artworks_available:
        return JsonResponse({"success": False, "error": "No artwork available to play game"})

    artwork = random.choice(artworks_available)
    request.session["artwork_id"] = artwork.id

    continents = Continent.objects.all().order_by("name")
    regions = Region.objects.select_related("continent").all().order_by("name")
    countries = Country.objects.select_related("region").all().order_by("name")

    return render(request, "game/play.html", {
        "artwork": artwork,
        "continents": continents,
        "regions": regions,
        "countries": countries,
    })


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

    user_sessions = (
        GameSession.objects
        .select_related("artwork")
        .filter(user=request.user)
        .order_by("-created_at")
    )

    correct_guesses = 0
    
    for session in user_sessions:
        correct_guesses += (session.score//20)

    user_history_data = {
        "user_sessions": user_sessions,
        "correct_guesses": correct_guesses}

    return render(request, "game/history.html", user_history_data)


@login_required(login_url='login')
def settings(request):
    return render(request, "game/profile_settings.html")



@staff_member_required(login_url='login')
def manage_users(request):
    users = User.objects.all().order_by("id")
    return render(request, "game/manage_users.html", {"users": users})

@staff_member_required(login_url='login')
def manage_artworks(request):
    artworks = Artwork.objects.select_related("artist", "country").all().order_by("id")
    return render(request, "game/manage_artworks.html", {"artworks": artworks})



@staff_member_required(login_url='login')
def enable_user(request):

    user_id = request.POST.get("user_id")

    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()

    return JsonResponse({"success": True, "status": "active"})
   

@staff_member_required(login_url='login')
def disable_user(request):
    
    user_id = request.POST.get("user_id")

    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()

    return JsonResponse({"success": True, "status": "disabled"})


@staff_member_required(login_url='login')
@require_POST
def add_artwork(request):

    title = request.POST.get("artwork-title", "").strip()
    image = request.POST.get("artwork-image", "").strip()  
    artist_name = request.POST.get("artwork-artist", "").strip()
    country_name = request.POST.get("artwork-country", "").strip()
    year = request.POST.get("artwork-year", "").strip()

    if not title or not image or not artist_name or not country_name or not year:
        return JsonResponse({"success": False, "message": "All fields required"})

    try:
        year = int(year)
    except ValueError:
        return JsonResponse({"success": False, "message": "Year must be a number"})

    country = get_object_or_404(Country, name__iexact=country_name)
    artist, _ = Artist.objects.get_or_create(name=artist_name)

    artwork = Artwork.objects.create(
        title=title,
        artist=artist,
        country=country,
        year=year,
        image=image
    )

    return JsonResponse({
        "success": True,
        "artwork": {
            "id": artwork.id,
            "title": artwork.title,
            "artist": artwork.artist.name,
            "country": artwork.country.name,
            "year": artwork.year
        }
    })


@staff_member_required(login_url='login')
@require_POST
def edit_artwork(request, artwork_id):

    artwork = get_object_or_404(Artwork, id=artwork_id)

    title = request.POST.get("artwork-title", "").strip()
    image = request.POST.get("artwork-image", "").strip()  
    artist_name = request.POST.get("artwork-artist", "").strip()
    country_name = request.POST.get("artwork-country", "").strip()
    year = request.POST.get("artwork-year", "").strip()

    if not title or not artist_name or not country_name or not year:
        return JsonResponse({"success": False, "message": "All fields required"})

    try:
        year = int(year)
    except ValueError:
        return JsonResponse({"success": False, "message": "Invalid year"})

    artwork = get_object_or_404(Artwork, name__iexact=artwork_id)
    country = get_object_or_404(Country, name__iexact=country_name)
    artist, created = Artist.objects.get_or_create(name=artist_name)

    artwork.title = title
    artwork.artist = artist
    artwork.country = country
    artwork.year = year

    if image:
        artwork.image = image

    artwork.save()

    return JsonResponse({
        "success": True,
        "artwork": {
            "id": artwork.id,
            "title": artwork.title,
            "artist": artwork.artist.name,
            "country": artwork.country.name,
            "year": artwork.year
        }
    })


@staff_member_required(login_url='login')
@require_POST
def delete_artwork(request, artwork_id):

    artwork = get_object_or_404(Artwork, id=artwork_id)
    artwork.delete()

    return JsonResponse({"success": True})


def artwork_information(request):
    artwork_info = request.session.get("last_artwork")
    return render(request, "game/art_info.html", {"artwork_info": artwork_info})
