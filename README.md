# StreetEasy Monitor
When looking for an apartment in New York City, it's important to be on top of new rental listings because competition is intense and good deals often come and go very quickly. It's a good idea to periodically check the sites where listings get posted, especially StreetEasy, which is where the majority of legitimate listings end up. This can be very time consuming, so this project aims to automate the process.

This project includes a script (`main.py`) that checks the search results for a URL matching selected filters (defined in `src/streeteasymonitor/scraper.py`), checks if any new listings have been posted, and automatically messages the listing agent using personalized form input defined in `.env`. After messaging the agent, the listing is stored in a database. The script checks for new posts by comparing the listings found in the search results against the listings stored in the database, and performs additional optional filtering if desired. [Supabase](https://github.com/supabase-community/supabase-py) is used for database operations.

A simple Flask application is included in the `app/` directory, which is served at `localhost:8000` by default. The purpose of the application is to monitor the search results based on a defined schedule using [Flask-APScheduler](https://viniciuschiele.github.io/flask-apscheduler/) to periodically execute `main.py`. The application defines a single route (`/`) which displays the listings that have been contacted, sorted by most recent. For each listing, the page shows when the agent was contacted, the address, the neighborhood, and the monthly rental price. If the rental has been indexed on [Paddaddy](https://paddaddy.app/), the address links to the corresponding page on Paddaddy is provided, and otherwise it links to the original StreetEasy listing.

## Table of Contents
- [Usage](#Usage)  
- [Installation](#Installation)
- [Configuration](#Configuration)  

## Usage

### Run Flask application
```
$ python -m app.app
```
By default the application will run on port 8000 and will continuously execute `main.py` at a random interval between 360 and 480 seconds until you quit the application

![screenshot](assets/screenshot.png)

### One-off script execution
```
$ python main.py
```

## Installation
### Clone project
```
$ git clone https://github.com/joeschermer/streeteasy-monitor.git
$ cd streeteasy-monitor
````
### (Recommended) Set up virtual environment using [pyenv](https://github.com/pyenv/)  

Install Python 3.12.3  
```
$ pyenv install 3.12.3
```
Create virtual environment
```
$ pyenv virtualenv 3.12.3 .streeteasy-monitor
```
Activate virtual environment
```
$ pyenv local .streeteasy-monitor
```


### Install requirements
```
$ pip install -r requirements.txt
```

## Configuration
### Create .env file
Add any necessary database credentials and message fields. Currently only works with Supabase but could be adapted for other databases/providers
```
$ touch .env
```
```
SUPABASE_URL=[YOUR SUPABASE URL]
SUPABASE_KEY=[YOUR SUPABASE KEY]

MESSAGE=[YOUR MESSAGE]
PHONE=[YOUR PHONE NUMBER]
EMAIL=[YOUR EMAIL ADDRESS]
NAME=[YOUR NAME]
```

### Add search URL and optional filters
Assign the `search_url` variable in `scraper.py` to your search URL filtered to your specifications using StreetEasy's interface
```
search_url = 'https://streeteasy.com/for-rent/nyc/[YOUR PARAMETERS]?sort_by=[YOUR SORTING METHOD]'
```
Add strings to the `filters` dictionary to filter substrings out of results not otherwise captured by StreetEasy (e.g. addresses with specific street names, URLs for "featured" listings that include the substring `'?featured=1'`)
```
filters = {
    'url': [YOUR FILTER STRINGS FOR URLS],
    'address': [YOUR FILTER STRINGS FOR ADDRESSES],
    'neighborhood': [YOUR FILTER STRINGS FOR NEIGHBORHOODS],
}
```