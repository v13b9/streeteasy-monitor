# StreetEasy Monitor
Python script that checks StreetEasy for new rentals matching search criteria and automatically messages new matches

### Features
- [Requests](https://pypi.org/project/requests/) Sessions with [fake-useragent](https://pypi.org/project/fake-useragent/) to bypass request blocking
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) for HTML parsing
- [environs](https://pypi.org/project/environs/) for environment variable parsing
- [Supabase Python Client](https://github.com/supabase-community/supabase-py) for database operations
- [Flask](https://flask.palletsprojects.com/en/3.0.x/) and [Flask-WTF](https://flask-wtf.readthedocs.io/en/1.2.x/) for simple web app implementation
- Integration with [Paddaddy](https://paddaddy.app/) for added rental info
- [Ruff](https://docs.astral.sh/ruff/) for code formatting
- Helper scripts for cron job management

## Table of Contents
- [Usage](#Usage)  
- [Installation](#Installation)
- [Configuration](#Configuration)  

## Usage

### One-off script execution
```bash
$ python main.py
```

### Run Flask application 
The application will run on port 8002 by default (can be changed in `app/app.py`).
```bash
$ python -m app.app
```
The application consists of:
- A form that can be used to check for listings based on specified criteria
- A table listing every rental that has been contacted so far, sorted by most recent

When possible, listings link to their corresponding page on [Paddaddy](https://paddaddy.app/), and otherwise link to the original page on StreetEasy.

![screenshot](assets/screenshot.png)

### (Optional) Create cron job
Setting up a cron job is the most straightforward way to run the script continuously, but I found it a little cumbersome, so I wrote some bash scripts to make the process a little easier.

Navigate to the cron folder and make all scripts executable
```bash
$ cd cron
$ chmod +x `ls *.sh`
```

Create cron job (the default configuration will run the script every 8 minutes)
```bash
$ ./create_cron.sh
```

Start the cron job
```bash
$ ./start_cron.sh
```

Stop the cron job
```bash
$ ./stop_cron.sh
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
$ pyenv virtualenv 3.12.3 .streeteasy-monitor
```
Activate virtual environment
```bash
$ pyenv local .streeteasy-monitor
```


### Install requirements
```bash
$ pip install -r requirements.txt
```

## Configuration
### Create .env file
Add any necessary database credentials and message fields. Currently only works with Supabase but could be adapted for other databases/providers
```bash
$ touch .env
```
```
SUPABASE_URL=[YOUR SUPABASE URL]
SUPABASE_KEY=[YOUR SUPABASE KEY]
```
```
MESSAGE=[YOUR MESSAGE]
PHONE=[YOUR PHONE NUMBER]
EMAIL=[YOUR EMAIL ADDRESS]
NAME=[YOUR NAME]
```
When the script runs, the listing agent for a given rental will be sent the above information, and you will receive an email indicating that the message has been sent.

### Configure default search parameters and optional filters
If you choose to run the script by itself or in a cron job, edit the `default` and `filters` dictionaries in `config.py` according to your preferences

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
    'address': ['Fulton', 'Atlantic', 'Herkimer'],
    'neighborhood': [
        'New Development',
        'Ocean Hill',
    ],
}
```
In this example, the script will check for rentals priced between $1,000 and $4,500, with 1-2 bedrooms, in the neighborhoods of Bedford-Stuyvesant, Carroll Gardens, and the Upper East Side. "Featured" listings will be excluded, and so will any apartments with addresses on Fulton, Atlantic, or Herkimer, or in the Ocean Hill sub-neighborhood.

### Configure cron helper scripts for script scheduling
The project includes a folder of shell scripts to help with managing a cron job based on `main.py`. This method allows the script to run without needing to run 
- `create_cron.sh`: Creates a cron command by selecting the full path of the correct Python interpreter based on the user's virtual environment, saving to `cron.dat`. By default the interval is 8 minutes but can be changed by reassigning `CRON_SCHEDULE`.
- `start_cron.sh`: Starts the cron job from `cron.dat`. The job will log stdout/stderr to `cron.log`
- `stop_cron.sh`: Stops any active cron job and saves to `cron.dat`