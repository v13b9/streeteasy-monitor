from datetime import datetime, timedelta, UTC

from dateutil.tz import gettz
from flask_bootstrap import Bootstrap5
from flask import Flask, request, redirect, render_template, session
import requests
import timeago

from src.streeteasymonitor.database import Database

from .forms import SearchForm

from main import main


def create_app():
    paddaddy_base_url = 'https://paddaddy.app'
    offermate_lookup_api = 'https://offermate.app/unit_lookup'

    app = Flask(__name__)
    bootstrap = Bootstrap5(app)
    db = Database()

    class FlaskConfig:
        SECRET_KEY = 'dev'

    app.config.from_object(FlaskConfig())

    @app.template_filter()
    def usd(value):
        """Format value as USD."""
        return f'${int(value):,}'

    @app.template_filter()
    def format_datetime(created_at):
        """Format date and time for current timezone."""
        local_tz = gettz()
        now = datetime.now(local_tz)
        parsed = datetime.fromisoformat(created_at).replace(tzinfo=UTC).astimezone()

        time_ago = timeago.format(parsed, now)

        date_formatted = parsed.strftime('%B %e, %Y')
        time_formatted = parsed.strftime('%l:%M %p')
        datetime_formatted = f'{date_formatted} {time_formatted}'

        return time_ago if now - parsed < timedelta(hours=8) else datetime_formatted

    @app.route('/', methods=['GET', 'POST'])
    def index():
        listings = db.get_listings_sorted()

        form = SearchForm()

        if request.method == 'POST':
            if form.validate_on_submit():
                kwargs = {
                    field.name: field.data or field.default
                    for field in form
                    if field.name != 'csrf_token' and field.name != 'submit'
                }
                session['data'] = kwargs
                main(**kwargs)
                return redirect('/')

            print('Invalid form submission\n')
            return redirect('/')
        
        data = session.pop('data', None)

        return render_template(
            'index.html',
            listings=listings,
            form=SearchForm(data=data),
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
