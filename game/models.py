from django.db import models

# Create your models here.

class Artist(models.Model):
    id = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)

class Continent(models.Model):
    id = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)

class Region(models.Model):
    id = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)
    continent = models.ForeignKey(Continent)

class Country(models.Model):
    id = models.IntegerField(unique=True)
    name = models.CharField(max_length=50, unique=True)
    region = models.ForeignKey(Region)

class Artwork(models.Model):
    id = models.IntegerField(unique=True)
    title = models.CharField(max_length=128)
    artist = models.ForeignKey(Artist)
    country = models.ForeignKey(Country)
    year = models.IntegerField()