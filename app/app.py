from datetime import datetime
from dateutil.tz import gettz
import random

from flask import Flask, render_template, redirect
from flask_apscheduler import APScheduler
from flask_session import Session
import requests
import timeago

from main import main
from src.streeteasymonitor.database import get_listings_sorted


PORT = 8000
app = Flask(__name__)

paddaddy_url = 'https://paddaddy.app'
offermate_lookup_api = 'https://offermate.app/unit_lookup'


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


class Config:
    SCHEDULER_API_ENABLED = True
    SCHEDULER_JOB_DEFAULTS = {'misfire_grace_time': None}


app.config.from_object(Config())


def create_app():
    # Configure session to use filesystem (instead of signed cookies)
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.remove_all_jobs()

    scheduler.add_job(
        id='main', func=main, trigger='interval', seconds=random.randint(360, 480)
    )

    scheduler.start()

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
        redirect_url = (
            paddaddy_url + json['matching_listings'][0]['url']
            if json.get('matching_listings')
            and json['matching_listings'][0]['similarity_type'] == 'exact_match'
            else url
        )
    except Exception as e:
        print(f'Error: {e}')
        redirect_url = url

    return redirect(redirect_url, code=302)


@app.route('/', methods=['GET'])
def index():
    listings = get_listings_sorted()
    return render_template('index.html', listings=listings)


if __name__ == '__main__':
    app = create_app()
    app.run(port=PORT)
