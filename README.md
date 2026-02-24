Local Setup

After cloning the repository, run:

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Steps:
migrate - creates the local database and applies all migrations
createsuperuser - creates your own login account
runserver - starts the development server

Then open:
http://127.0.0.1:8000/checkins/
Log in with the user you created and test:
  Create, edit, and delete check-ins
Visit the Progress page: /checkins/progress/
Test API endpoints:
  /checkins/api/progress/
  /checkins/api/checkins/

Each team member will have their own local database.
