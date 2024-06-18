# StreetEasy Monitor
Python script that checks StreetEasy for new rentals matching search criteria and automatically messages new matches.

Includes a Flask application that provides a search interface and displays contacted listings, plus optional helper scripts for setting up a cron job.

### Features
- Uses a [Requests](https://pypi.org/project/requests/) Session with [fake-useragent](https://pypi.org/project/fake-useragent/) to bypass request blocking
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) for HTML parsing
- [Supabase Python Client](https://github.com/supabase-community/supabase-py) for database operations
- [environs](https://pypi.org/project/environs/) for environment variable parsing
- [Flask](https://flask.palletsprojects.com/en/3.0.x/), [Flask-WTF](https://flask-wtf.readthedocs.io/en/1.2.x/), and [Choices.js](https://github.com/Choices-js/Choices) for simple web app implementation
- Integration with [Paddaddy](https://paddaddy.app/) for added rental info
- Helper scripts for cron job management
- [Ruff](https://docs.astral.sh/ruff/) for code formatting

## Table of Contents
- [Usage](#Usage)  
- [Installation](#Installation)
- [Configuration](#Configuration)  

## Usage

### One-off script execution
```bash
(.venv) $ python main.py
```

### Run Flask application 
The application will run on port 8002 by default (can be changed in `app/app.py`).
```bash
(.venv) $ python -m app.app
```
The application consists of:
- A form that can be used to check for listings based on specified criteria
- A table listing every rental that has been contacted so far, sorted by most recent

When possible, listings link to their corresponding page on [Paddaddy](https://paddaddy.app/), and otherwise link to the original page on StreetEasy.

![screenshot](assets/screenshot.png)

### (Optional) Create cron job
Setting up a cron job is the most straightforward way to run the script continuously, but it can be a cumbersome process. A collection of bash scripts are included to help streamline the process.

Navigate to the cron folder and make all scripts executable
```bash
(.venv) $ cd cron
(.venv) $ chmod +x `ls *.sh`
```

Create cron job

<i>Note: if using a virtual environment, it must be activated for the script to select the correct Python path.</i>
```bash
(.venv) $ ./create_cron.sh
```

Start the cron job
```bash
(.venv) $ ./start_cron.sh
```

Stop the cron job
```bash
(.venv) $ ./stop_cron.sh
```

## Installation
### Clone project
```bash
$ git clone https://github.com/joeschermer/streeteasy-monitor.git
$ cd streeteasy-monitor
````
### (Recommended) Install Python and set up virtual environment using [pyenv](https://github.com/pyenv/)  
Install Python 3.12.3  
```bash
$ pyenv install 3.12.3
```
Create virtual environment
```bash
$ pyenv virtualenv 3.12.3 .venv
```
Activate virtual environment
```bash
$ pyenv local .venv
```

### Install requirements
```bash
(.venv) $ pip install -r requirements.txt
```

## Configuration
### Create .env file
```bash
$ touch .env
```
Add database credentials (by default, requires a Supabase account and proper database schema defining a table named `listings`).

Adapt to your desired database as needed by editing `database.py`.
```
SUPABASE_URL=[YOUR SUPABASE URL]
SUPABASE_KEY=[YOUR SUPABASE KEY]
```

Add your desired message, along with your phone number, email, and name. All fields are required.
```
MESSAGE=[YOUR MESSAGE]
PHONE=[YOUR PHONE NUMBER]
EMAIL=[YOUR EMAIL ADDRESS]
NAME=[YOUR NAME]
```
When the script runs, the listing agent for a matching rental will be sent the above information, and you will receive an automated email from StreetEasy at the address you provided indicating that the message has been sent.

### Configure default search parameters and optional filters
If you choose to run the script by itself or in a cron job, edit the `default` and `filters` dictionaries in `config.py` according to your preferences.

- `default`: defines the parameters that will be used when running the script directly (i.e., not through the Flask form)
- `filters`: defines substrings for filtering results not otherwise captured by StreetEasy (e.g. addresses on specific streets, URLs for "featured" listings which include the substring `'?featured=1'`)

Example:

```python
default = {
    'min_price': 1000,
    'max_price': 4500,
    'min_beds': 1,
    'max_beds': 2,
    'areas': [
        'Bedford-Stuyvesant',
        'Carroll Gardens',
        'Upper East Side',
    ],
}

filters = {
    'url': ['?featured=1', '?infeed=1'],
    'address': [
        'Fulton',
        'Atlantic',
        'Herkimer',
    ],
    'neighborhood': [
        'New Development',
        'Ocean Hill',
    ],
}
```
In this example, the script will check for rentals priced between $1,000 and $4,500, with 1-2 bedrooms, in the neighborhoods of Bedford-Stuyvesant, Carroll Gardens, and the Upper East Side. "Featured" listings will be excluded, and so will any rentals with addresses on Fulton, Atlantic, or Herkimer, or in the Ocean Hill sub-neighborhood.

### Configure cron helper scripts for script scheduling
The `cron/` directory contains the following files, which can be configured according to your preferences if using a cron job.
- `create_cron.sh`: Saves a cron table entry to `cron.dat`. By default the cron job will run `main.py` every 8 minutes, but can be changed by reassigning `CRON_SCHEDULE`.
- `start_cron.sh`: Starts the cron job from `cron.dat`. The job will log stdout/stderr to `cron.log` by default.
- `stop_cron.sh`: Stops any active cron job and saves to `cron.dat`.