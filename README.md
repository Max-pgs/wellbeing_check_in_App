Deployment

Deployed application:

https://wellbeing-check-in-app.onrender.com

Repository

Source code:

https://github.com/Max-pgs/wellbeing_check_in_App

Local Setup

After cloning the repository, install dependencies and apply migrations:

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver

Steps

pip install -r requirements.txt

Installs the required Python packages for the project.

python manage.py migrate

Creates the local database and applies all migrations.

python manage.py createsuperuser

Creates an administrator account for logging into the application and Django admin.

python manage.py runserver

Starts the local development server.

Access the application

Then open:

http://127.0.0.1:8000/checkins/

Log in with the user you created and test the main features:

create, edit, and delete check-ins

manage goals and habits

view progress analytics

browse check-in history

Useful pages

Main application:

http://127.0.0.1:8000/checkins/

Progress page:

http://127.0.0.1:8000/checkins/progress/

API endpoints:

http://127.0.0.1:8000/checkins/api/progress/

http://127.0.0.1:8000/checkins/api/checkins/

Django admin:

http://127.0.0.1:8000/admin/

Notes

Each team member has their own local development database.

Local development uses SQLite by default.

The deployed application on Render uses PostgreSQL for persistent data storage.
