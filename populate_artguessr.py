#heavily inspired by populate_rango.py
import os
os.environ.setdefault("DJANGO.SETTINGS_MODULE", "config.settings")

def populate():
    artists = [
        {"name":"Leonardo da Vinci"},
        {"name":"Michelangelo"},
        {"name":"Charles Edward Wilson"},
        {"name":"Andy Warhol"},
        {"name":"Katsushika Hokusai"},
        {"name":"Chéri Samba"},
        {"name":"Araceli Gilbert"}
    ]
    continents = [
        {"name":"South America"},
        {"name":"North America"},
        {"name":"Europe"},
        {"name":"Africa"},
        {"name":"Asia"},
        {"name":"Oceania"}
    ]
    regions = [
        {
            "name":"South America",
            "continent":"South America"
        },
        {
            "name":"Caribbean",
            "continent":"North America"
        },
        {
            "name":"Central America",
            "continent":"North America"
        },
        {
            "name":"Northern America",
            "continent":"North America",
        },
        {
            "name":"Western Europe",
            "continent":"Europe"
        },
        {
            "name":"Southern Europe",
            "continent":"Europe"
        },
        {
            "name":"Northern Europe",
            "continent":"Europe"
        },
        {
            "name":"Eastern Europe",
            "continent":"Europe"
        },
        {
            "name":"Northern Africa",
            "continent":"Africa"
        },
        {
            "name":"Western Africa",
            "continent":"Africa"
        },
        {
            "name":"Central Africa",
            "continent":"Africa"
        },
        {
            "name":"Eastern Africa",
            "continent":"Africa"
        },
        {
            "name":"Southern Africa",
            "continent":"Africa"
        },
        {
            "name":"Central Asia",
            "continent":"Asia"
        },
        {
            "name":"Western Asia",
            "continent":"Asia"
        },
        {
            "name":"Southern Asia",
            "continent":"Asia"
        },
        {
            "name":"Central Asia",
            "continent":"Asia"
        },
        {
            "name":"Southeastern Asia",
            "continent":"Asia"
        },
        {
            "name":"Micronesia",
            "continent":"Oceania"
        },
        {
            "name":"Polynesia",
            "continent":"Oceania"
        },
        {
            "name":"Melanesia",
            "continent":"Oceania"
        },
        {
            "name":"Australia and New Zealand",
            "continent":"Oceania"
        }
    ]