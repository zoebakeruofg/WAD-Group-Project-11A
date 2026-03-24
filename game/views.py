from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from .models import AdminProfile

# Create your views here.

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

def play(request):

    context = {}

    return render(request, "game/play.html", context)

def leaderboard(request):

    context = {}

    return render(request, "game/leaderboard.html", context)

def history(request):

    context = {}

    return render(request, "game/history.html", context)

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