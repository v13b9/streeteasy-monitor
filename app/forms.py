from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, IntegerField, SubmitField
from wtforms.validators import NumberRange, InputRequired

neighborhoods = {
    'Brooklyn': [
        'Carroll Gardens',
        'Clinton Hill',
        'Cobble Hill',
        'Crown Heights',
        'Fort Greene',
        'Gowanus',
        'Greenpoint',
        'Park Slope',
        'Prospect Heights',
        'Prospect Lefferts Gardens',
        'Williamsburg',
        'Bedford-Stuyvesant',
        'Boerum Hill',
        'DUMBO',
        'Downtown Brooklyn',
        'Brooklyn Heights',
    ],
    'Manhattan': [
        'Lower East Side',
        'Upper East Side',
    ],
    'Queens': [
        'Ridgewood',
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
