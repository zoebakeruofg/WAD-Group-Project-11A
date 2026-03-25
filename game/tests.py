from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import (
    Artist,
    AdminProfile,
    Continent,
    Region,
    Country,
    Artwork,
    GameSession,
)


class ModelTests(TestCase):

    def setUp(self):
        """
        Create basic objects used in multiple tests
        """

        self.continent = Continent.objects.create(name="Europe")

        self.region = Region.objects.create(
            name="Western Europe",
            continent=self.continent
        )

        self.country = Country.objects.create(
            name="Netherlands",
            region=self.region
        )

        self.artist = Artist.objects.create(
            name="Vincent van Gogh"
        )

        self.artwork = Artwork.objects.create(
            title="Starry Night",
            artist=self.artist,
            country=self.country,
            year=1889,
            image_url="https://example.com/starrynight.jpg"
        )

    def test_artist_creation(self):
        """Artist should be created correctly"""
        self.assertEqual(self.artist.name, "Vincent van Gogh")
        self.assertEqual(str(self.artist), "Vincent van Gogh")

    def test_continent_creation(self):
        """Continent should be created correctly"""
        self.assertEqual(self.continent.name, "Europe")
        self.assertEqual(str(self.continent), "Europe")

    def test_region_relationship(self):
        """Region should correctly link to Continent"""
        self.assertEqual(self.region.continent, self.continent)
        self.assertEqual(self.region.continent.name, "Europe")

    def test_country_relationship(self):
        """Country should correctly link to Region"""
        self.assertEqual(self.country.region, self.region)
        self.assertEqual(self.country.region.name, "Western Europe")

    def test_artwork_relationships(self):
        """Artwork should correctly link to Artist and Country"""
        self.assertEqual(self.artwork.artist, self.artist)
        self.assertEqual(self.artwork.country, self.country)

    def test_artwork_fields(self):
        """Artwork fields should store correct values"""
        self.assertEqual(self.artwork.title, "Starry Night")
        self.assertEqual(self.artwork.year, 1889)
        self.assertEqual(self.artwork.image_url, "https://example.com/starrynight.jpg")

    def test_artwork_str_method(self):
        """Artwork __str__ should return title"""
        self.assertEqual(str(self.artwork), "Starry Night")

class ViewTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_play_requires_login(self):
        response = self.client.get(reverse("play"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_leaderboard_requires_login(self):
        response = self.client.get(reverse("leaderboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_history_requires_login(self):
        response = self.client.get(reverse("history"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_register_page_loads(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_logout_redirects_to_home(self):
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))


class RegisterTests(TestCase):
    def test_register_success_regular_user(self):
        response = self.client.post(reverse("register"), {
            "email": "user1@example.com",
            "username": "user1",
            "password": "testpass123",
            "confirm_password": "testpass123",
            "account_type": "user",
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(User.objects.filter(username="user1").exists())

        user = User.objects.get(username="user1")
        self.assertFalse(user.is_staff)

    def test_register_fails_with_missing_fields(self):
        response = self.client.post(reverse("register"), {
            "email": "",
            "username": "user2",
            "password": "testpass123",
            "confirm_password": "testpass123",
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="user2").exists())

    def test_register_fails_when_passwords_do_not_match(self):
        response = self.client.post(reverse("register"), {
            "email": "user3@example.com",
            "username": "user3",
            "password": "testpass123",
            "confirm_password": "wrongpass",
            "account_type": "user",
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="user3").exists())

    def test_register_fails_when_username_exists(self):
        User.objects.create_user(
            username="existinguser",
            email="old@example.com",
            password="testpass123"
        )

        response = self.client.post(reverse("register"), {
            "email": "new@example.com",
            "username": "existinguser",
            "password": "testpass123",
            "confirm_password": "testpass123",
            "account_type": "user",
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(username="existinguser").count(), 1)

    def test_register_fails_when_email_exists(self):
        User.objects.create_user(
            username="olduser",
            email="same@example.com",
            password="testpass123"
        )

        response = self.client.post(reverse("register"), {
            "email": "same@example.com",
            "username": "newuser",
            "password": "testpass123",
            "confirm_password": "testpass123",
            "account_type": "user",
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="newuser").exists())

    def test_register_success_admin_user_with_valid_guid(self):
        response = self.client.post(reverse("register"), {
            "email": "admin1@example.com",
            "username": "admin1",
            "password": "testpass123",
            "confirm_password": "testpass123",
            "account_type": "admin",
            "guid": "3010809L",
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

        user = User.objects.get(username="admin1")
        self.assertTrue(user.is_staff)
        self.assertTrue(AdminProfile.objects.filter(user=user).exists())

    def test_register_fails_admin_with_invalid_guid(self):
        response = self.client.post(reverse("register"), {
            "email": "admin2@example.com",
            "username": "admin2",
            "password": "testpass123",
            "confirm_password": "testpass123",
            "account_type": "admin",
            "guid": "INVALID123",
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="admin2").exists())


class LoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="normaluser",
            email="normal@example.com",
            password="testpass123"
        )

        self.admin_user = User.objects.create_user(
            username="adminuser",
            email="admin@example.com",
            password="testpass123"
        )
        self.admin_user.is_staff = True
        self.admin_user.save()

        AdminProfile.objects.create(
            user=self.admin_user,
            guid="3010809L"
        )

    def test_login_success_regular_user(self):
        response = self.client.post(reverse("login"), {
            "username": "normaluser",
            "password": "testpass123",
            "role": "user",
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

    def test_login_fails_with_wrong_password(self):
        response = self.client.post(reverse("login"), {
            "username": "normaluser",
            "password": "wrongpassword",
            "role": "user",
        })

        self.assertEqual(response.status_code, 200)

    def test_login_fails_for_disabled_user(self):
        self.user.is_active = False
        self.user.save()

        response = self.client.post(reverse("login"), {
            "username": "normaluser",
            "password": "testpass123",
            "role": "user",
        })

        self.assertEqual(response.status_code, 200)

    def test_login_fails_when_regular_user_tries_admin_role(self):
        response = self.client.post(reverse("login"), {
            "username": "normaluser",
            "password": "testpass123",
            "role": "admin",
            "guid": "3010809L",
        })

        self.assertEqual(response.status_code, 200)

    def test_login_fails_when_admin_logs_in_as_user(self):
        response = self.client.post(reverse("login"), {
            "username": "adminuser",
            "password": "testpass123",
            "role": "user",
        })

        self.assertEqual(response.status_code, 200)

    def test_login_fails_when_admin_guid_missing(self):
        response = self.client.post(reverse("login"), {
            "username": "adminuser",
            "password": "testpass123",
            "role": "admin",
            "guid": "",
        })

        self.assertEqual(response.status_code, 200)

    def test_login_fails_when_admin_guid_invalid(self):
        response = self.client.post(reverse("login"), {
            "username": "adminuser",
            "password": "testpass123",
            "role": "admin",
            "guid": "WRONGGUID",
        })

        self.assertEqual(response.status_code, 200)

    def test_login_fails_when_admin_guid_does_not_match_profile(self):
        response = self.client.post(reverse("login"), {
            "username": "adminuser",
            "password": "testpass123",
            "role": "admin",
            "guid": "3075329W",
        })

        self.assertEqual(response.status_code, 200)

    def test_login_success_admin_user(self):
        response = self.client.post(reverse("login"), {
            "username": "adminuser",
            "password": "testpass123",
            "role": "admin",
            "guid": "3010809L",
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))


class MakeGuessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="guessuser",
            password="testpass123"
        )

        self.continent = Continent.objects.create(name="Europe")
        self.region = Region.objects.create(
            name="Western Europe",
            continent=self.continent
        )
        self.country = Country.objects.create(
            name="Netherlands",
            region=self.region
        )
        self.artist = Artist.objects.create(name="Vincent van Gogh")

        self.artwork = Artwork.objects.create(
            title="Starry Night",
            artist=self.artist,
            country=self.country,
            year=1889,
            image_url="https://example.com/starrynight.jpg"
        )

    def test_make_guess_requires_login(self):
        response = self.client.post(reverse("make_guess"), {
            "continent": "Europe",
            "region": "Western Europe",
            "country": "Netherlands",
            "artist": "Vincent van Gogh",
            "year": "1889",
        })

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_make_guess_without_artwork_id_returns_error_json(self):
        self.client.login(username="guessuser", password="testpass123")

        response = self.client.post(reverse("make_guess"), {
            "continent": "Europe",
            "region": "Western Europe",
            "country": "Netherlands",
            "artist": "Vincent van Gogh",
            "year": "1889",
        })

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], "No artwork available")

    def test_make_guess_all_correct_score_100_and_creates_session(self):
        self.client.login(username="guessuser", password="testpass123")

        session = self.client.session
        session["artwork_id"] = self.artwork.id
        session.save()

        response = self.client.post(reverse("make_guess"), {
            "continent": "Europe",
            "region": "Western Europe",
            "country": "Netherlands",
            "artist": "Vincent van Gogh",
            "year": "1889",
        })

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertTrue(data["success"])
        self.assertEqual(data["score"], 100)
        self.assertEqual(GameSession.objects.count(), 1)

    def test_make_guess_saves_last_result_and_last_artwork_in_session(self):
        self.client.login(username="guessuser", password="testpass123")

        session = self.client.session
        session["artwork_id"] = self.artwork.id
        session.save()

        response = self.client.post(reverse("make_guess"), {
            "continent": "Europe",
            "region": "Western Europe",
            "country": "Netherlands",
            "artist": "Vincent van Gogh",
            "year": "1889",
        })

        self.assertEqual(response.status_code, 200)

        session = self.client.session
        self.assertIn("last_result", session)
        self.assertIn("last_artwork", session)


class ResultTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="resultuser",
            password="testpass123"
        )

    def test_result_requires_login(self):
        response = self.client.get(reverse("result"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_result_page_loads_when_logged_in(self):
        self.client.login(username="resultuser", password="testpass123")

        response = self.client.get(reverse("result"))
        self.assertEqual(response.status_code, 200)


class HistoryTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="historyuser1",
            password="testpass123"
        )
        self.user2 = User.objects.create_user(
            username="historyuser2",
            password="testpass123"
        )

        self.continent = Continent.objects.create(name="Europe")
        self.region = Region.objects.create(
            name="Western Europe",
            continent=self.continent
        )
        self.country = Country.objects.create(
            name="Netherlands",
            region=self.region
        )
        self.artist = Artist.objects.create(name="Vincent van Gogh")

        self.artwork = Artwork.objects.create(
            title="Starry Night",
            artist=self.artist,
            country=self.country,
            year=1889,
            image_url="https://example.com/starrynight.jpg"
        )

        GameSession.objects.create(
            user=self.user1,
            artwork=self.artwork,
            guess_continent="europe",
            guess_country="netherlands",
            guess_artist="vincent van gogh",
            guess_year=1889,
            score=80
        )

        GameSession.objects.create(
            user=self.user2,
            artwork=self.artwork,
            guess_continent="asia",
            guess_country="japan",
            guess_artist="wrong artist",
            guess_year=1900,
            score=0
        )

    def test_history_requires_login(self):
        response = self.client.get(reverse("history"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_history_shows_only_current_user_sessions(self):
        self.client.login(username="historyuser1", password="testpass123")

        response = self.client.get(reverse("history"))
        self.assertEqual(response.status_code, 200)

        user_sessions = response.context["user_sessions"]
        self.assertEqual(user_sessions.count(), 1)
        self.assertEqual(user_sessions.first().user, self.user1)