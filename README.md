# Stock Market Service API endpoint

API endpoint app using Django REST. It'll query against Alpha Vantage's daily timeseries API using a valid NASDAQ symbol.

## Running the app through the cloud

The app is deployed in Heroku and can be accessed through the following [link](https://ahd-stockmarketservice.herokuapp.com/).

## Running the app locally

To run the app locally, you'll need [Python 3.9](https://www.python.org/downloads/release/python-3913/) installed. Once done, follow the following steps:

- Clone or download the repository to a local path.
- Open a command line application and change directory to the local path where the repository was downloaded. An example in Windows would be: \
	`cd C:\Users\UserName\Documents\Python\stockmarketservice`
- Download the package requirements from the requirements.txt file: \
`pip install -r requirements.txt`
- Run the server locally through the following command: \
`python manage.py runserver`
- A similar message as the following should appear, with the local IP address where the app is running:

> Watching for file changes with StatReloader\
> Performing system checks...\
> \
> System check identified no issues (0 silenced).\
> August 01, 2022 - 14:18:18\
> Django version 3.2.14, using settings 'stockmarketservice.settings'\
> Starting development server at http://127.0.0.1:8000/ \
> Quit the server with CTRL-BREAK.

- Enter the IP address returned in a web browser to open the app.

### API logs

When running the app locally, API calls will be logged in the following file inside the root directory of the application: **stockmarketservice.log**
