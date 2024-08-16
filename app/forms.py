from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, IntegerField, SubmitField, BooleanField
from wtforms.validators import NumberRange, InputRequired

neighborhoods = {
    "Brooklyn": [
        "Greenpoint",
        "Williamsburg",
        "Downtown Brooklyn",
        "Fort Greene",
        "Brooklyn Heights",
        "Boerum Hill",
        "DUMBO",
        "Vinegar Hill",
        "Bedford-Stuyvesant",
        "Stuyvesant Heights",
        "Bushwick",
        "East New York",
        "Red Hook",
        "Park Slope",
        "Gowanus",
        "Carroll Gardens",
        "Cobble Hill",
        "Sunset Park",
        "Windsor Terrace",
        "Crown Heights",
        "Prospect Heights",
        "Weeksville",
        "Prospect Lefferts Gardens",
        "Bay Ridge",
        "Dyker Heights",
        "Fort Hamilton",
        "Bensonhurst",
        "Borough Park",
        "Kensington",
        "Coney Island",
        "Brighton Beach",
        "Flatbush",
        "Cypress Hills",
        "Midwood",
        "Ocean Hill",
        "Brownsville",
        "Prospect Park South",
        "East Flatbush",
        "Canarsie",
        "Flatlands",
        "Marine Park",
        "Clinton Hill",
        "East Williamsburg",
    ],
    "Manhattan": [
        "Financial District",
        "Tribeca",
        "Stuyvesant Town/PCV",
        "Soho",
        "Little Italy",
        "Lower East Side",
        "Chinatown",
        "Two Bridges",
        "Battery Park City",
        "Chelsea",
        "Greenwich Village",
        "East Village",
        "Noho",
        "Midtown",
        "Midtown South",
        "Midtown East",
        "Midtown West",
        "Murray Hill",
        "Kips Bay",
        "Upper West Side",
        "Upper East Side",
        "Hudson Yards",
        "Morningside Heights",
        "Hamilton Heights",
        "Washington Heights",
        "Inwood",
        "Hell's Kitchen",
        "West Harlem",
        "Central Harlem",
        "East Harlem",
        "West Village",
        "Flatiron",
        "NoMad",
        "Nolita",
    ],
    "Queens": [
        "Astoria",
        "Long Island City",
        "Sunnyside",
        "Woodside",
        "Jackson Heights",
        "Elmhurst",
        "Corona",
        "Maspeth",
        "Middle Village",
        "Ridgewood",
        "Glendale",
        "Rego Park",
        "Forest Hills",
        "Flushing",
        "Ditmars-Steinway",
    ],
}

extras = {
    'pets': 'Pets allowed',
    'doorman': 'Doorman',
    'laundry': 'Laundry',
    'elevator': 'Elevator',
    'private_outdoor_space': 'Private outdoor space',
    'dishwasher': 'Dishwasher',
    'washer_dryer': 'Washer dryer',
    'gym': 'Gym',
}

class SearchForm(FlaskForm):
    min_price = IntegerField(
        'Minimum Price',
        default=0,
        validators=[
            NumberRange(
                min=0,
                max=10000,
                message='test',
            ),
        ],
        render_kw={
            'step': '100',
            'placeholder': 'Min price',
            'class': 'form-control',
        },
    )
    max_price = IntegerField(
        'Maximum Price',
        validators=[
            InputRequired(),
            NumberRange(
                min=0,
                max=10000,
            ),
        ],
        render_kw={
            'step': '100',
            'placeholder': 'Max price',
            'class': 'form-control',
        },
    )
    min_beds = IntegerField(
        'Minimum Beds',
        validators=[
            InputRequired(),
            NumberRange(
                min=0,
                max=4,
            ),
        ],
        render_kw={
            'placeholder': 'Min beds',
            'class': 'form-control',
        },
    )
    max_beds = IntegerField(
        'Maximum Beds',
        validators=[
            InputRequired(),
            NumberRange(
                min=0,
                max=4,
            ),
        ],
        render_kw={
            'placeholder': 'Max beds',
            'class': 'form-control',
        },
    )
    areas = SelectMultipleField(
        'Neighborhoods',
        choices=neighborhoods,
        validators=[InputRequired()],
        render_kw={
            'placeholder': 'Select neighborhoods',
        },
    )
    baths = IntegerField(
        'Minimum Bathrooms',
        default=0,
        validators=[
            NumberRange(
                min=0,
                max=4,
            ),
        ],
        render_kw={
            'placeholder': 'Min baths',
            'class': 'form-control',
        },
    )
    amenities = SelectMultipleField(
        'Amenities',
        choices=list(extras.items()),
        render_kw={
            'placeholder': 'Select amenities',
        },
    )
    no_fee = BooleanField(
        'No fee',
        render_kw={
            'class': 'form-check-input',
        },
    )

    submit = SubmitField('Run')
