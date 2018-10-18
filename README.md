# tkapi-explorer-server

Explorer of the Tweede Kamer (Dutch parliament) Open Data Portaal (OData API).
It allows developers to view relations and available data in the OData API.

Requires Python 3.4+ and Django 2.0+

## Installation (Linux)

Get the code and enter the project directory,
```
git clone https://github.com/bartromgens/petanque-stats-server.git
cd petanque-stats-server
```

Install dependencies that you will need,
```
apt install virtualenv
```

Create a virtual environment,
```
virtualenv -p python3 env
```

Activate the virtualenv (always do this before working on the project),
```
source env/bin/activate
```

Install python packages in the local env,
```
pip install --upgrade pip
pip install -r requirements.txt
```

Generate a `local_settings.py` file from the example,
```
python create_local_settings.py
```

Create a database (default is sqlite),
```
python manage.py migrate
```

#### Run a development webserver
Run the Django dev web server in the virtualenv (don't forget to active the virtualenv),
```
python manage.py runserver
```

The API is now available at http://127.0.0.1:8000/v1/.

## Configuration (optional)

#### local_settings.py

The local settings are defined in `api/local_settings.py`.
These are not under version control and you are free change these for your personal needs.
This is also the place for secret settings. An example, on which this file is based, is found in `api/local_settings_example.py`.

## Testing

Run all tests,
```
python manage.py test
```

Run specific tests (example),
```
python manage.py test api.tests.<TestClass>.<test_function>
```
