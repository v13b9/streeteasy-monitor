from flask import Flask, render_template
from flask_session import Session

from src.streeteasier.database import get_listings


def usd(value):
    """Format value as USD."""
    return f'${value:,}'


app = Flask(__name__)

app.jinja_env.filters['usd'] = usd

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
    return render_template('index.html', listings=get_listings())


if __name__ == '__main__':
    app.run(debug=True)
