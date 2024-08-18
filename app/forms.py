from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, IntegerField, SubmitField, BooleanField
from wtforms.validators import NumberRange, InputRequired, Optional

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
        'Min Price',
        validators=[
            InputRequired(),
            NumberRange(
                min=0,
                max=10000,
                message=('test'),
            ),
        ],
        render_kw={
            'step': '100',
            'placeholder': 'Min',
            'class': 'form-control',
        },
    )
    max_price = IntegerField(
        'Max Price',
        validators=[
            InputRequired(),
            NumberRange(
                min=100,
                max=10000,
            ),
        ],
        render_kw={
            'step': '100',
            'placeholder': 'Max',
            'class': 'form-control',
        },
    )
    no_fee = BooleanField(
        'No fee',
        validators=[Optional()],
        render_kw={
            'class': 'form-check-input',
        },
    )
    min_beds = IntegerField(
        'Min Beds',
        validators=[
            InputRequired(),
            NumberRange(
                min=0,
                max=4,
            ),
        ],
        render_kw={
            'placeholder': 'Min',
            'class': 'form-control',
        },
    )
    max_beds = IntegerField(
        'Max Beds',
        validators=[
            InputRequired(),
            NumberRange(
                min=0,
                max=4,
            ),
        ],
        render_kw={
            'placeholder': 'Max',
            'class': 'form-control',
        },
    )
    baths = IntegerField(
        'Bathrooms',
        validators=[
            InputRequired(),
            NumberRange(
                min=0,
                max=4,
            ),
        ],
        render_kw={
            'placeholder': 'Min',
            'class': 'form-control',
        },
    )
    areas = SelectMultipleField(
        'Neighborhoods',
        choices=neighborhoods,
        validators=[InputRequired()],
        render_kw={
            'placeholder': 'Select neighborhoods',
            'class': 'form-select',
        },
    )
    amenities = SelectMultipleField(
        'Amenities',
        default=[],
        choices=list(extras.items()),
        validators=[Optional()],
        render_kw={
            'placeholder': 'Select amenities',
            'class': 'form-select',
        },
    )

    submit = SubmitField('Run')
