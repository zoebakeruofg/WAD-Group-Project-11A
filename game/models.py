from django.db import models
from django.contrib.auth.models import User

class Artist(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class AdminProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="admin_profile"
    )
    guid = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.user.username} - {self.guid}"


class Continent(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=50)
    continent = models.ForeignKey(
        Continent,
        on_delete=models.CASCADE,
        related_name="regions"
    )

    def __str__(self):
        return self.name


class Country(models.Model):
    class Meta:
        verbose_name_plural = "Countries"
        def __str__(self):
            return self.name
    name = models.CharField(max_length=50, unique=True)
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="countries"
    )

    def __str__(self):
        return self.name


class Artwork(models.Model):
    title = models.CharField(max_length=128)
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="artworks"
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="artworks"
    )
    year = models.IntegerField()
    image_url = models.URLField(blank=True)

    def __str__(self):
        return self.title

class GameSession(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sessions"
    )

    artwork = models.ForeignKey(
        Artwork,
        on_delete=models.CASCADE
    )

    guess_continent = models.CharField(max_length=50, blank=True)
    guess_country = models.CharField(max_length=50, blank=True)
    guess_artist = models.CharField(max_length=50, blank=True)
    guess_year = models.IntegerField(null=True, blank=True)

    score = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.artwork.title}"
