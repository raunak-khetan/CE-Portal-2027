# CE Portal

The CE Portal is the Alcheringa “Highway to Alcher” website. It presents city
and competition information, accepts solo and team registrations, and hosts a
multi-step CFA registration form.

## Features

- Browse competition locations, event details, dates, and deadlines.
- Register for solo events or create a team and add its members.
- Manage city/event registration status and competition data in Django Admin.
- Submit CFA registrations through a three-step form.
- View registration data through Django Admin and its import/export tools.

## Tech stack

- Python 3.11; Django 4.2.5
- Django templates, CSS, and JavaScript; no separate frontend build step
- SQLite by default for local development; production database configured
  through `DATABASE_URL` (PostgreSQL support is included)
- MinIO for production static and uploaded media storage
- Gunicorn for serving the application in the container

## Project structure

```text
cityelimination/             Project settings and root URL, WSGI, and ASGI config
  settings.py                Database, static/media, email, and environment settings
core/                        Main Django app
  models.py                  Cities, events, registrations, teams, and CFA data
  views.py                   Competition pages, registration, and CFA workflows
  forms.py                   Registration forms and validation
  admin.py                   Admin screens and import/export configuration
  migrations/                Database schema history
  management/commands/      Commands for loading sample competition data
templates/core/              Django HTML pages
static/                      CSS, JavaScript, fonts, video, and image assets
media/                       Uploaded media files
manage.py                    Django command-line entry point
requirements.txt             Python dependencies
Dockerfile                   Container image definition
runserver.sh                 Container startup (migrations, static collection, Gunicorn)
```

## Run locally

Prerequisite: Python 3.11. From the repository root:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/>. Local settings use SQLite in `db.sqlite3` and
store uploaded media under `media/`.

Optional setup:

```sh
python manage.py seed_test_events   # Load sample cities and competitions
python manage.py createsuperuser    # Create an admin login
```

Then visit <http://127.0.0.1:8000/admin/> to manage site data.

## Useful routes and commands

- `/` — competition landing page
- `/competitions/` — competition listing
- `/cfa/` — CFA registration
- `/admin/` — Django administration
- `/api/cities/` and `/get-events/<city_name>/` — city/event data endpoints

Run Django's configuration and test checks with:

```sh
python manage.py check
python manage.py test
```

## Configuration and privacy

The site sends registration confirmation emails through SMTP. Configure
`EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` in your local environment to test
email delivery; registration submission will not be saved if sending fails.
Production also requires database and storage credentials. Keep all credentials
and personal data out of source control and README examples; provide secrets
through environment configuration instead.