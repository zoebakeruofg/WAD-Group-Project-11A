import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from game.models import Continent, Region, Country, Artist

def run():
    # Continents
    europe, _ = Continent.objects.get_or_create(name="Europe")
    asia, _ = Continent.objects.get_or_create(name="Asia")

    # Regions
    western_europe, _ = Region.objects.get_or_create(name="Western Europe", continent=europe)
    southern_europe, _ = Region.objects.get_or_create(name="Southern Europe", continent=europe)
    eastern_asia, _ = Region.objects.get_or_create(name="Eastern Asia", continent=asia)

    # Countries
    Country.objects.get_or_create(name="Italy", region=southern_europe)
    Country.objects.get_or_create(name="France", region=western_europe)
    Country.objects.get_or_create(name="Spain", region=southern_europe)
    Country.objects.get_or_create(name="Netherlands", region=western_europe)
    Country.objects.get_or_create(name="China", region=eastern_asia)
    Country.objects.get_or_create(name="Japan", region=eastern_asia)

    # Artists
    Artist.objects.get_or_create(name="Leonardo da Vinci")
    Artist.objects.get_or_create(name="Vincent van Gogh")
    Artist.objects.get_or_create(name="Pablo Picasso")
    Artist.objects.get_or_create(name="Claude Monet")
    Artist.objects.get_or_create(name="Hokusai")

    print("Database populated successfully ✅")

if __name__ == "__main__":
    run()
