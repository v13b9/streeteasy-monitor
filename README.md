# StreetEasy Monitor
When looking for an apartment in New York City, it's important to be on top of new rental listings because competition is intense and good deals often come and go very quickly. It's a good idea to periodically check the sites where listings get posted, especially StreetEasy, which is where the majority of legitimate listings end up. This can be very time consuming, so this project aims to automate the process.

This project includes a script (`main.py`) that checks the search results for a URL matching selected filters (defined in `src/streeteasymonitor/scraper.py`), checks if any new listings have been posted, and automatically messages the listing agent using personalized form input defined in `.env`. After messaging the agent, the listing is stored in a database. The script checks for new posts by comparing the listings found in the search results against the listings stored in the database, and performs additional optional filtering if desired. [Supabase](https://github.com/supabase-community/supabase-py) is used for database operations.

A simple Flask application is included in the `app/` directory, which is served at `localhost:8000` by default. The purpose of the application is to monitor the search results based on a defined schedule using [Flask-APScheduler](https://viniciuschiele.github.io/flask-apscheduler/) to periodically execute `main.py`. The application defines a single route (`/`) which displays the listings that have been contacted, sorted by most recent. For each listing, the page shows when the agent was contacted, the address, the neighborhood, and the monthly rental price. If the rental has been indexed on [Paddaddy](https://paddaddy.app/), the address links to the corresponding page on Paddaddy is provided, and otherwise it links to the original StreetEasy listing.

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
```bash
$ python -m app.app
```
By default the application will run on port 8000 and will continuously execute `main.py` at a random interval between 360 and 480 seconds until you quit the application

![screenshot](assets/screenshot.png)

### (Optional) Create cron job
Navigate to the cron folder and make all scripts executable
```bash
$ cd cron
$ chmod +x `ls *.sh`
```

Create cron job (by default this sets the script to execute every minute)
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
### (Recommended) Set up virtual environment using [pyenv](https://github.com/pyenv/)  

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

MESSAGE=[YOUR MESSAGE]
PHONE=[YOUR PHONE NUMBER]
EMAIL=[YOUR EMAIL ADDRESS]
NAME=[YOUR NAME]
```

### Add search URL and optional filters
Assign the `search_url` variable in `scraper.py` to your search URL filtered to your specifications using StreetEasy's interface
```python
search_url = 'https://streeteasy.com/for-rent/nyc/[YOUR PARAMETERS]?sort_by=[YOUR SORTING METHOD]'
```
Add strings to the `filters` dictionary to filter substrings out of results not otherwise captured by StreetEasy (e.g. addresses with specific street names, URLs for "featured" listings that include the substring `'?featured=1'`)
```python
filters = {
    'url': [YOUR FILTER STRINGS FOR URLS],
    'address': [YOUR FILTER STRINGS FOR ADDRESSES],
    'neighborhood': [YOUR FILTER STRINGS FOR NEIGHBORHOODS],
}
```
### (Optional) Configure cron helper scripts for script scheduling
The project includes a folder of shell scripts to help with managing a cron job based on `main.py`. This method allows the script to run without needing to run 
- `create_cron.sh`: Creates a cron command by selecting the full path of the correct Python interpreter based on the user's virtual environment, saving to `cron.dat`. By default the interval is 1 minute but can be changed by reassigning `CRON_SCHEDULE`.
- `start_cron.sh`: Starts the cron job from `cron.dat`. The job will log stdout/stderr to `cron.log`
- `stop_cron.sh`: Stops any active cron job and saves to `cron.dat` 