from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


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


