## Deployment

Deployed application:  

https://wellbeing-check-in-app.onrender.com

## Repository

Source code:  

https://github.com/Max-pgs/wellbeing_check_in_App

## Local Setup

The project can be run locally either by cloning the repository or by extracting the ZIP file.

After downloading or extracting the project, open a terminal and move into the folder that contains `manage.py`.

Example on Windows:

```cmd
cd wellbeing_check_in_App-main
cd wellbeing_check_in_app

1. Create and activate a virtual environment

if you use Windows (Command Prompt):

python -m venv .venv

.venv\Scripts\activate

if you use Windows (PowerShell):

python -m venv .venv

.\.venv\Scripts\Activate.ps1

if you use macOS / Linux:

python3 -m venv .venv

source .venv/bin/activate

2. Upgrade pip

python -m pip install --upgrade pip

3. Install dependencies

pip install -r requirements.txt

4. Apply migrations

python manage.py migrate

5. Create a superuser account

python manage.py createsuperuser

6. Start the development server

python manage.py runserver

Access the Application

Then open:

http://127.0.0.1:8000/

Log in with the user you created and test the main features:

create, edit, and delete check-ins

manage goals and habits

view progress analytics

browse check-in history

Useful Pages

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

- Local development uses SQLite by default.

- The deployed application on Render uses PostgreSQL for persistent data storage.

- Each team member can work with their own local development database.

- If dependencies fail to install, make sure Python 3.8 or above is being used.
