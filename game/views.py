from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import random
from django.contrib.admin.views.decorators import staff_member_required
from .models import Artwork, Artist, Country, Region, Continent
from .models import Artwork, GameSession, AdminProfile
from django.db.models import Avg


ALLOWED_ADMIN_GUIDS = {
    "3010809L",
    "3075329W",
    "3012337L",
    "2961000A",
    "2975768B",
}


def home(request):
    return render(request, "game/home.html")


@login_required(login_url='login')
def play(request):
    artworks = Artwork.objects.all()

    if not artworks:
        return render(request, "game/play.html", {"artwork": None})

    artwork = random.choice(artworks)
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
def leaderboard(request):
    leaderboard_data = (
        GameSession.objects
        .values("user__username")
        .annotate(avg_score=Avg("score"))
        .order_by("-avg_score", "user__username")
    )

    leaderboard_rows = []
    for entry in leaderboard_data:
        leaderboard_rows.append({
            "username": entry["user__username"],
            "avg_score": round(entry["avg_score"], 2) if entry["avg_score"] is not None else 0,
        })

    context = {
        "leaderboard_rows": leaderboard_rows
    }

    return render(request, "game/leaderboard.html", context)

@login_required(login_url='login')
def history(request):

    user_sessions = (
        GameSession.objects
        .select_related("artwork")
        .filter(user=request.user)
        .order_by("-created_at")
    )

    for session in user_sessions:
        session.correct_guesses = session.score // 25

    context = {
        "user_sessions": user_sessions
    }

    return render(request, "game/history.html", context)


def result(request):
    result_data = request.session.get("last_result")
    return render(request, "game/result.html", {"result_data": result_data})


@login_required(login_url='login')
def profile_settings(request):
    return render(request, "game/profile_settings.html")


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


@staff_member_required(login_url='login')
@require_POST
def delete_artwork(request, artwork_id):
    try:
        artwork = Artwork.objects.get(id=artwork_id)
        artwork.delete()
        return JsonResponse({"success": True})
    except Artwork.DoesNotExist:
        return JsonResponse({"success": False, "message": "Artwork not found."})


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

@staff_member_required(login_url='login')
def manage_users(request):
    users = User.objects.all().order_by("id")
    return render(request, "game/manage_users.html", {"users": users})


@staff_member_required(login_url='login')
def manage_artworks(request):
    artworks = Artwork.objects.select_related("artist", "country").all().order_by("id")
    return render(request, "game/manage_artworks.html", {"artworks": artworks})

@staff_member_required(login_url='login')
@require_POST
def enable_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = True
        user.save()

        return JsonResponse({
            "success": True,
            "status": "Active"
        })
    except User.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "User not found."
        })


@staff_member_required(login_url='login')
@require_POST
def disable_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)

        if user == request.user:
            return JsonResponse({
                "success": False,
                "message": "You cannot disable your own admin account."
            })

        user.is_active = False
        user.save()

        return JsonResponse({
            "success": True,
            "status": "Disabled"
        })
    except User.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "User not found."
        })


def art_info(request):
    artwork_info = request.session.get("last_artwork_info")
    return render(request, "game/art_info.html", {"artwork_info": artwork_info})


@login_required(login_url='login')
@require_POST
def submit_guess(request):
    continent_guess = request.POST.get("continent", "").strip()
    region_guess = request.POST.get("region", "").strip()
    country_guess = request.POST.get("country", "").strip()
    artist_guess = request.POST.get("artist", "").strip()
    year_guess = request.POST.get("year", "").strip()

    artwork_id = request.session.get("artwork_id")

    if not artwork_id:
        return JsonResponse({
            "success": False,
            "message": "No active artwork found."
        })

    try:
        artwork = Artwork.objects.get(id=artwork_id)
    except Artwork.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "Artwork not found."
        })

    correct_continent = artwork.country.region.continent.name
    correct_region = artwork.country.region.name
    correct_country = artwork.country.name
    correct_artist = artwork.artist.name
    correct_year = str(artwork.year)

    score = 0

    if continent_guess.lower() == correct_continent.lower():
        score += 20
    if region_guess.lower() == correct_region.lower():
        score += 20
    if country_guess.lower() == correct_country.lower():
        score += 20
    if artist_guess.lower() == correct_artist.lower():
        score += 20
    if year_guess == correct_year:
        score += 20

    if request.user.is_authenticated:
        GameSession.objects.create(
            user=request.user,
            artwork=artwork,
            guess_continent=continent_guess,
            guess_region=region_guess,
            guess_country=country_guess,
            guess_artist=artist_guess,
            guess_year=int(year_guess) if year_guess.isdigit() else None,
            score=score
        )

    request.session["last_result"] = {
        "score": score,
        "guesses": {
            "continent": continent_guess,
            "region": region_guess,
            "country": country_guess,
            "artist": artist_guess,
            "year": year_guess,
        },
        "correct_answers": {
            "continent": correct_continent,
            "region": correct_region,
            "country": correct_country,
            "artist": correct_artist,
            "year": correct_year,
        }
    }

    request.session["last_artwork_info"] = {
        "title": artwork.title,
        "artist": artwork.artist.name,
        "country": artwork.country.name,
        "region": artwork.country.region.name,
        "continent": artwork.country.region.continent.name,
        "year": artwork.year,
        "image_url": artwork.image.url if artwork.image else "",
    }

    return JsonResponse({
        "success": True,
        "score": score,
        "guesses": {
            "continent": continent_guess,
            "region": region_guess,
            "country": country_guess,
            "artist": artist_guess,
            "year": year_guess,
        },
        "correct_answers": {
            "continent": correct_continent,
            "region": correct_region,
            "country": correct_country,
            "artist": correct_artist,
            "year": correct_year,
        },
        "artwork_info": {
            "title": artwork.title,
            "artist": artwork.artist.name,
            "country": artwork.country.name,
            "region": artwork.country.region.name,
            "continent": artwork.country.region.continent.name,
            "year": artwork.year,
            "image_url": artwork.image.url if artwork.image else "",
        }
    })
    
@staff_member_required(login_url='login')
@require_POST
def add_artwork(request):
    title = request.POST.get("title", "").strip()
    artist_name = request.POST.get("artist", "").strip()
    country_name = request.POST.get("country", "").strip()
    year = request.POST.get("year", "").strip()
    image = request.FILES.get("image")

    if not title or not artist_name or not country_name or not year:
        return JsonResponse({
            "success": False,
            "message": "Please fill in all required fields."
        })

    try:
        year = int(year)
    except ValueError:
        return JsonResponse({
            "success": False,
            "message": "Year must be a number."
        })

    artist, created = Artist.objects.get_or_create(name=artist_name)

    try:
        country = Country.objects.get(name__iexact=country_name)
    except Country.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "Country not found. Please use an existing country."
        })

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
    title = request.POST.get("title", "").strip()
    artist_name = request.POST.get("artist", "").strip()
    country_name = request.POST.get("country", "").strip()
    year = request.POST.get("year", "").strip()
    image = request.FILES.get("image")

    if not title or not artist_name or not country_name or not year:
        return JsonResponse({
            "success": False,
            "message": "Please fill in all required fields."
        })

    try:
        year = int(year)
    except ValueError:
        return JsonResponse({
            "success": False,
            "message": "Year must be a number."
        })

    try:
        artwork = Artwork.objects.get(id=artwork_id)
    except Artwork.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "Artwork not found."
        })

    artist, created = Artist.objects.get_or_create(name=artist_name)

    try:
        country = Country.objects.get(name__iexact=country_name)
    except Country.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "Country not found. Please use an existing country."
        })

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