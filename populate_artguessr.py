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
    #Regions are as defined by https://en.wikipedia.org/wiki/United_Nations_geoscheme
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
            "name":"Middle Africa",
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
            "name":"Eastern Asia",
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
    northern_africa = ["Algeria",
                       "Egypt",
                       "Libya",
                       "Morocco",
                       "Sudan",
                       "Tunisia"]
    eastern_africa = ["Burundi",
                      "Comoros",
                      "Djibouti",
                      "Eritrea",
                      "Ethiopia",
                      "Kenya",
                      "Madagascar",
                      "Malawi",
                      "Mauritius",
                      "Mozambique",
                      "Rwanda",
                      "Seychelles",
                      "Somalia",
                      "South Sudan",
                      "Uganda", 
                      "Tanzania",
                      "Zambia",
                      "Zimbabwe"]
    middle_africa = ["Angola",
                     "Cameroon",
                     "Central African Republic",
                     "Chad",
                     "Congo",
                     "DR Congo",
                     "Equitoreal Guinea",
                     "Gabon",
                     "São Tomé and Principe"]
    southern_africa = ["Botswana",
                       "Eswatini",
                       "Lesotho",
                       "Namibia",
                       "South Africa"]
    western_africa = ["Benin",
                      "Burkina Faso",
                      "Cabo Verde",
                      "Côte d'Ivoire",
                      "Gambia",
                      "Ghana",
                      "Guinea",
                      "Guinea-Bissau",
                      "Liberia",
                      "Mali",
                      "Mauritania",
                      "Niger",
                      "Nigeria",
                      "Senegal",
                      "Sierra Leone",
                      "Togo"]
    caribbean = ["Antigua and Barbadua",
                 "Bahamas",
                 "Barbados",
                 "Cuba",
                 "Dominica",
                 "Dominican Republic",
                 "Grenada",
                 "Haiti",
                 "Jamaica",
                 "Saint Kitts and Nevis",
                 "Saint Lucia",
                 "Saint Vincent and the Grenadines",
                 "Trinidad and Tobago"]
    central_america = ["Belize",
                       "Costa Rica",
                       "El Salvador",
                       "Guatemala",
                       "Honduras",
                       "Mexico",
                       "Nicaragua",
                       "Panama"]
    south_america = ["Argentina",
                     "Bolivia",
                     "Brazil",
                     "Chile",
                     "Colombia",
                     "Ecuador",
                     "Guyana",
                     "Paraguay",
                     "Peru",
                     "Suriname",
                     "Uruguay",
                     "Venezuela"]
    northern_america = ["Canada", "United States of America"]
    central_asia = ["Kazakhstan",
                    "Kyrgyzstan",
                    "Tajikistan",
                    "Uzbekistan"]
    eastern_asia = ["China",
                    "North Korea",
                    "Japan",
                    "Mongolia",
                    "South Korea"]
    southeastern_asia = ["Brunei",
                         "Cambodia",
                         "Indonesia",
                         "Laos",
                         "Malaysia",
                         "Myanmar",
                         "Phillipines",
                         "Singapore",
                         "Thailand",
                         "East Timor",
                         "Vietnam"]
    southern_asia = ["Afghanistan",
                    "Bangladesh",
                    "Bhutan",
                    "India",
                    "Iran",
                    "Maldives",
                    "Nepal",
                    "Pakistan",
                    "Sri Lanka"]
    western_asia = ["Armenia",
                    "Azerbaijan",
                    "Bahrain",
                    "Cyprus",
                    "Georgia",
                    "Iraq",
                    "Israel",
                    "Jordan",
                    "Kuwait",
                    "Lebanon",
                    "Oman",
                    "Palestine",
                    "Qatar",
                    "Saudi Arabia",
                    "Syria",
                    "Türkiye",
                    "United Arab Emirates",
                    "Yemen"]
    eastern_europe = ["Belarus",
                      "Bulgaria",
                      "Czechia",
                      "Hungary",
                      "Poland",
                      "Moldova",
                      "Romania",
                      "Romania",
                      "Russia",
                      "Slovakia",
                      "Ukraine"]
    northern_europe = ["Denmark",
                       "Estonia",
                       "Finland",
                       "Iceland",
                       "Ireland",
                       "Latvia",
                       "Lithuania",
                       "Norway",
                       "Sweden",
                       "United Kingdom"]
    southern_europe = ["Albania",
                       "Andorra",
                       "Bosnia and Herzegovina",
                       "Croatia",
                       "Greece",
                       "Vatican City",
                       "Italy",
                       "Kosovo",
                       "Malta",
                       "Montenegro",
                       "North Macedonia",
                       "Portugal",
                       "San Marino",
                       "Serbia",
                       "Slovenia",
                       "Spain"]
    western_europe = ["Austria",
                      "Belgium",
                      "France",
                      "Germany",
                      "Liechtenstein",
                      "Luxembourg",
                      "Monaco",
                      "Netherlands",
                      "Switzerland"]
    australia_and_new_zealand = ["Australia", "New Zealand"]
    melanesia = ["Fiji",
                 "Papua New Guinea",
                 "Solomon Islands",
                 "Vanuatu"]
    micronesia = ["Kiribati",
                  "Marshall Islands",
                  "Micronesia",
                  "Nauru",
                  "Palau",
                  "Samoa",
                  "Tonga",
                  "Tuvalu"]