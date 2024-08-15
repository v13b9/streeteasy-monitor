from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, IntegerField, SubmitField
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

class SearchForm(FlaskForm):
    min_price = IntegerField(
        'Minimum Price',
        validators=[
            InputRequired(),
            NumberRange(
                min=0,
                max=10000,
                message='test',
            ),
        ],
        render_kw={
            'step': '100',
            'placeholder': 'Min price',
        },
    )
    max_price = IntegerField(
        'Maximum Price',
        validators=[
            InputRequired(),
            NumberRange(
                min=0,
                max=10000,
                message='test',
            ),
        ],
        render_kw={
            'step': '100',
            'placeholder': 'Max price',
        },
    )
    min_beds = IntegerField(
        'Minimum Beds',
        validators=[
            InputRequired(),
            NumberRange(
                min=0,
                max=4,
                message='test',
            ),
        ],
        render_kw={
            'placeholder': 'Min beds',
        },
    )
    max_beds = IntegerField(
        'Maximum Beds',
        validators=[
            InputRequired(),
            NumberRange(
                min=0,
                max=4,
                message='test',
            ),
        ],
        render_kw={
            'placeholder': 'Max beds',
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
    submit = SubmitField('Run')
