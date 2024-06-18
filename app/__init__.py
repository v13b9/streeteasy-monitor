from datetime import datetime
import json

from dateutil.tz import gettz
from flask import Flask, request, redirect, render_template
import requests
import timeago

from src.streeteasymonitor.config import Config
from src.streeteasymonitor.database import Database
from .forms import SearchForm
from main import main


def create_app():
    paddaddy_base_url = 'https://paddaddy.app'
    offermate_lookup_api = 'https://offermate.app/unit_lookup'

    app = Flask(__name__)

    config = Config()
    db = Database(config)

    class FlaskConfig:
        SECRET_KEY = 'dev'

    app.config.from_object(FlaskConfig())

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
    
    @app.route('/', methods=['GET', 'POST'])
    def index():
        listings = db.get_listings_sorted()
        form = SearchForm()

        if request.method == 'POST':
            if form.validate_on_submit():
                kwargs = {
                    field.name: field.data
                    for field in form
                    if field.name != 'csrf_token' and field.name != 'submit'
                }

                print(f'Running script with kwargs:\n{json.dumps(kwargs, indent=2)}')
                main(**kwargs)
                return redirect('/')

            print(f'Invalid form submission\n')
            return redirect('/')

        return render_template(
            'index.html',
            listings=listings,
            form=form,
        )

    @app.route('/<path:url>', methods=['GET'])
    def url(url):
        try:
            params = {'q': url}
            r = requests.get(offermate_lookup_api, params=params)
            json = r.json()
            if (
                json.get('matching_listings')
                and json['matching_listings'][0]['similarity_type'] == 'exact_match'
            ):
                paddaddy_id = json['matching_listings'][0]['url']
                redirect_url = paddaddy_base_url + paddaddy_id
            else:
                redirect_url = url
        except Exception as e:
            print(f'Error: {e}')
            redirect_url = url

        return redirect(redirect_url, code=302)

    return app
