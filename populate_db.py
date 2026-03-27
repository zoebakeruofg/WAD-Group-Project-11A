import os
import django
 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
 
from game.models import Continent, Region, Country, Artist
 
 
def run():
    artists = [
        "Leonardo da Vinci",
        "Michelangelo",
        "Vincent van Gogh",
        "Rembrandt",
        "Johannes Vermeer",
        "Edvard Munch",
        "Gustav Klimt",
        "Katsushika Hokusai",
        "Pablo Picasso",
        "Claude Monet",
    ]
 
    continents = [
        "South America",
        "North America",
        "Europe",
        "Africa",
        "Asia",
        "Oceania",
    ]
 
    regions = [
        {"name": "South America", "continent": "South America"},
        {"name": "Caribbean", "continent": "North America"},
        {"name": "Central America", "continent": "North America"},
        {"name": "Northern America", "continent": "North America"},
        {"name": "Western Europe", "continent": "Europe"},
        {"name": "Southern Europe", "continent": "Europe"},
        {"name": "Northern Europe", "continent": "Europe"},
        {"name": "Eastern Europe", "continent": "Europe"},
        {"name": "Northern Africa", "continent": "Africa"},
        {"name": "Western Africa", "continent": "Africa"},
        {"name": "Middle Africa", "continent": "Africa"},
        {"name": "Eastern Africa", "continent": "Africa"},
        {"name": "Southern Africa", "continent": "Africa"},
        {"name": "Western Asia", "continent": "Asia"},
        {"name": "Southern Asia", "continent": "Asia"},
        {"name": "Central Asia", "continent": "Asia"},
        {"name": "Southeastern Asia", "continent": "Asia"},
        {"name": "Eastern Asia", "continent": "Asia"},
        {"name": "Micronesia", "continent": "Oceania"},
        {"name": "Polynesia", "continent": "Oceania"},
        {"name": "Melanesia", "continent": "Oceania"},
        {"name": "Australia and New Zealand", "continent": "Oceania"},
    ]
 
    northern_africa = [
        "Algeria", "Egypt", "Libya", "Morocco", "Sudan", "Tunisia"
    ]
    eastern_africa = [
        "Burundi", "Comoros", "Djibouti", "Eritrea", "Ethiopia", "Kenya",
        "Madagascar", "Malawi", "Mauritius", "Mozambique", "Rwanda",
        "Seychelles", "Somalia", "South Sudan", "Uganda", "Tanzania",
        "Zambia", "Zimbabwe"
    ]
    middle_africa = [
        "Angola", "Cameroon", "Central African Republic", "Chad", "Congo",
        "DR Congo", "Equitoreal Guinea", "Gabon", "São Tomé and Principe"
    ]
    southern_africa = [
        "Botswana", "Eswatini", "Lesotho", "Namibia", "South Africa"
    ]
    western_africa = [
        "Benin", "Burkina Faso", "Cabo Verde", "Côte d'Ivoire", "Gambia",
        "Ghana", "Guinea", "Guinea-Bissau", "Liberia", "Mali", "Mauritania",
        "Niger", "Nigeria", "Senegal", "Sierra Leone", "Togo"
    ]
    caribbean = [
        "Antigua and Barbadua", "Bahamas", "Barbados", "Cuba", "Dominica",
        "Dominican Republic", "Grenada", "Haiti", "Jamaica",
        "Saint Kitts and Nevis", "Saint Lucia",
        "Saint Vincent and the Grenadines", "Trinidad and Tobago"
    ]
    central_america = [
        "Belize", "Costa Rica", "El Salvador", "Guatemala", "Honduras",
        "Mexico", "Nicaragua", "Panama"
    ]
    south_america = [
        "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador",
        "Guyana", "Paraguay", "Peru", "Suriname", "Uruguay", "Venezuela"
    ]
    northern_america = ["Canada", "United States of America"]
    central_asia = ["Kazakhstan", "Kyrgyzstan", "Tajikistan", "Uzbekistan"]
    eastern_asia = ["China", "North Korea", "Japan", "Mongolia", "South Korea"]
    southeastern_asia = [
        "Brunei", "Cambodia", "Indonesia", "Laos", "Malaysia", "Myanmar",
        "Phillipines", "Singapore", "Thailand", "East Timor", "Vietnam"
    ]
    southern_asia = [
        "Afghanistan", "Bangladesh", "Bhutan", "India", "Iran", "Maldives",
        "Nepal", "Pakistan", "Sri Lanka"
    ]
    western_asia = [
        "Armenia", "Azerbaijan", "Bahrain", "Cyprus", "Georgia", "Iraq",
        "Israel", "Jordan", "Kuwait", "Lebanon", "Oman", "Palestine",
        "Qatar", "Saudi Arabia", "Syria", "Türkiye",
        "United Arab Emirates", "Yemen"
    ]
    eastern_europe = [
        "Belarus", "Bulgaria", "Czechia", "Hungary", "Poland", "Moldova",
        "Romania", "Russia", "Slovakia", "Ukraine"
    ]
    northern_europe = [
        "Denmark", "Estonia", "Finland", "Iceland", "Ireland", "Latvia",
        "Lithuania", "Norway", "Sweden", "United Kingdom"
    ]
    southern_europe = [
        "Albania", "Andorra", "Bosnia and Herzegovina", "Croatia", "Greece",
        "Vatican City", "Italy", "Kosovo", "Malta", "Montenegro",
        "North Macedonia", "Portugal", "San Marino", "Serbia", "Slovenia",
        "Spain"
    ]
    western_europe = [
        "Austria", "Belgium", "France", "Germany", "Liechtenstein",
        "Luxembourg", "Monaco", "Netherlands", "Switzerland"
    ]
    australia_and_new_zealand = ["Australia", "New Zealand"]
    melanesia = ["Fiji", "Papua New Guinea", "Solomon Islands", "Vanuatu"]
    polynesia = ["Tonga", "Samoa", "Tuvalu"]
    micronesia = ["Kiribati", "Marshall Islands", "Micronesia", "Nauru", "Palau"]
 
    regions_countries = {
        "Northern Africa": northern_africa,
        "Eastern Africa": eastern_africa,
        "Middle Africa": middle_africa,
        "Southern Africa": southern_africa,
        "Western Africa": western_africa,
        "Caribbean": caribbean,
        "Central America": central_america,
        "South America": south_america,
        "Northern America": northern_america,
        "Central Asia": central_asia,
        "Eastern Asia": eastern_asia,
        "Southeastern Asia": southeastern_asia,
        "Southern Asia": southern_asia,
        "Western Asia": western_asia,
        "Eastern Europe": eastern_europe,
        "Northern Europe": northern_europe,
        "Southern Europe": southern_europe,
        "Western Europe": western_europe,
        "Australia and New Zealand": australia_and_new_zealand,
        "Melanesia": melanesia,
        "Micronesia": micronesia,
        "Polynesia": polynesia,
    }
 
    def add_continent(name):
        return Continent.objects.get_or_create(name=name)[0]
 
    def add_region(name, continent):
        return Region.objects.get_or_create(name=name, continent=continent)[0]
 
    def add_country(name, region):
        return Country.objects.get_or_create(name=name, region=region)[0]
 
    def add_artist(name):
        return Artist.objects.get_or_create(name=name)[0]
 
    continent_lookup = {}
    for continent_name in continents:
        continent_lookup[continent_name] = add_continent(continent_name)
 
    region_lookup = {}
    for region in regions:
        continent_obj = continent_lookup[region["continent"]]
        region_obj = add_region(region["name"], continent_obj)
        region_lookup[region["name"]] = region_obj
 
    for region_name, countries in regions_countries.items():
        region_obj = region_lookup[region_name]
        for country_name in countries:
            add_country(country_name, region_obj)
 
    for artist_name in artists:
        add_artist(artist_name)
 
    print("Database populated successfully ✅")
    print("Continents:", Continent.objects.count())
    print("Regions:", Region.objects.count())
    print("Countries:", Country.objects.count())
    print("Artists:", Artist.objects.count())
 
 
if __name__ == "__main__":
    run()