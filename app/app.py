from datetime import datetime
from dateutil.tz import gettz
import random

from flask import Flask, request, render_template, redirect
from flask_apscheduler import APScheduler
from flask_session import Session
from flask_wtf import CSRFProtect, FlaskForm
import requests
import timeago
from wtforms import SelectMultipleField, IntegerField, SubmitField
from wtforms.validators import NumberRange, InputRequired

from main import main
from src.streeteasymonitor.database import Database
from src.streeteasymonitor.config import Config

paddaddy_base_url = 'https://paddaddy.app'
offermate_lookup_api = 'https://offermate.app/unit_lookup'

app = Flask(__name__)


config = Config()
db = Database(config)


# hostname = 'aws-0-us-east-1.pooler.supabase.com'
# port = 5432
# database = 'postgres'
# username = 'postgres.omszflfpoxotqapvioim'
# password = 'JF1Ew9aTJZkPisIh'

# db = PostgreSQL(hostname=hostname, port=port, database=database, username=username, password=password)


@app.template_filter()
def usd(value):
    """Format value as USD."""
    return f'${value:,}'


@app.template_filter()
def format_datetime(created_at):
    """Format date and time for current timezone."""
    NYC = gettz('America/New_York')
    now = datetime.now(NYC)

    parsed = datetime.fromisoformat(created_at).astimezone(NYC)
    date_formatted = parsed.strftime('%B %e, %Y')
    time_formatted = parsed.strftime('%l:%M %p')

    time_ago = timeago.format(parsed, now)

    delta = now - parsed
    hours = delta.total_seconds() / 3600

    datetime_formatted = f'{date_formatted} {time_formatted}'

    return datetime_formatted if hours > 8 else time_ago


def create_app():
    class Config:
        SCHEDULER_API_ENABLED = True
        SCHEDULER_JOB_DEFAULTS = {'misfire_grace_time': None}
        SECRET_KEY = 'test'
        SESSION_PERMANENT = False
        SESSION_TYPE = 'filesystem'

    app.config.from_object(Config())

    Session(app)
    # csrf = CSRFProtect(app)

    # scheduler = APScheduler()
    # scheduler.init_app(app)
    # scheduler.remove_all_jobs()

    # scheduler.add_job(
    #     id='main',
    #     func=main,
    #     trigger='interval',
    #     seconds=random.randint(360, 480)
    # )

    # scheduler.start()

    return app


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = 0
    response.headers['Pragma'] = 'no-cache'
    return response


@app.route('/<path:url>', methods=['GET'])
def url(url):
    try:
        params = {'q': url}
        r = requests.get(offermate_lookup_api, params=params)
        json = r.json()
        if json.get('matching_listings') and json['matching_listings'][0]['similarity_type'] == 'exact_match':
            paddaddy_id = json['matching_listings'][0]['url']
            redirect_url = paddaddy_base_url + paddaddy_id
        else:
            redirect_url = url
    except Exception as e:
        print(f"Error: {e}")
        redirect_url = url

    return redirect(redirect_url, code=302)


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
    ]
}


class SearchForm(FlaskForm):
    min_price = IntegerField(
        'Minimum Price',
        validators=[
            InputRequired(),
            NumberRange(min=0, max=10000, message='test'),
            ],
        render_kw={
            "step": "100",
            "placeholder": "Min price",
            },
        )
    max_price = IntegerField(
        'Maximum Price',
        validators=[
            InputRequired(),
            NumberRange(min=0, max=10000, message='test'),
            ],
        render_kw={
            "step": "100",
            "placeholder": "Max price",
            },
        )
    min_beds = IntegerField(
        'Minimum Beds',
        validators=[
            InputRequired(),
            NumberRange(min=0, max=4, message='test'),
            ],
        render_kw={
            "placeholder": "Min beds",
            },
        )
    max_beds = IntegerField(
        'Maximum Beds',
        validators=[
            InputRequired(),
            NumberRange(min=0, max=4, message='test'),
            ],
        render_kw={
            "placeholder": "Max beds",
            },
        )
    areas = SelectMultipleField(
        'Neighborhoods',
        choices=neighborhoods,
        validators=[
            InputRequired()
            ],
        render_kw={
            "placeholder": "Select neighborhoods",
            },
        )
    submit = SubmitField('Run')


@app.route('/', methods=['GET', 'POST'])
def index():
    listings = db.get_listings_sorted()
    form = SearchForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            search_parameters = {
                field.name: field.data
                for field in form
                if field.name != 'csrf_token' and field.name != 'submit'
                }

            print(f'search_parameters: {search_parameters}')
            main(**search_parameters)
        return redirect('/')
    
    return render_template(
        'index.html',
        listings=listings,
        form=form,
    )

PORT = 8002

if __name__ == '__main__':
    app = create_app()
    
    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=True
        )
