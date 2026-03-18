from django.contrib import admin
from .models import Artist, Continent, Region, Country, Artwork, GameSession

admin.site.register(Artist)
admin.site.register(Continent)
admin.site.register(Region)
admin.site.register(Country)
admin.site.register(Artwork)
admin.site.register(GameSession)