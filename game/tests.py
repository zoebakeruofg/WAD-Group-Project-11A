from django.test import TestCase
from .models import Artist, Continent, Region, Country, Artwork

from django.test import TestCase
from .models import Artist, Continent, Region, Country, Artwork


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
