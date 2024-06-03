from datetime import datetime
from dateutil.tz import gettz
import random

from flask import Flask, render_template
from flask_session import Session
from flask_apscheduler import APScheduler

from main import main
from src.streeteasier.database import get_listings_sorted


def usd(value):
    """Format value as USD."""
    return f'${value:,}'


def format_datetime(created_at):
    """Format date and time for current timezone."""
    NYC = gettz('America/New_York')
    parsed = datetime.fromisoformat(created_at).astimezone(NYC)
    date_formatted = parsed.strftime('%B %e, %Y')
    time_formatted = parsed.strftime('%l:%M %p')
    return f'{date_formatted} {time_formatted}'


# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True
    SCHEDULER_JOB_DEFAULTS = {'misfire_grace_time': None}


app = Flask(__name__)
app.config.from_object(Config())
app.jinja_env.filters = {
    'usd': usd,
    'format_datetime': format_datetime,
}


# Configure session to use filesystem (instead of signed cookies)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = 0
    response.headers['Pragma'] = 'no-cache'
    return response


@app.route('/')
def index():
    return render_template('index.html', listings=get_listings_sorted())


if __name__ == '__main__':
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.remove_all_jobs()

    scheduler.add_job(
        id='main',
        func=main,
        trigger='interval',
        minutes=random.randint(6, 8)
    )

    scheduler.start()

    app.run()
