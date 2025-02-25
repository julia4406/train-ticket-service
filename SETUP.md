# Setup Guide

Follow these steps to set up and run this project on your local machine.

## Prerequisites

Ensure you have the following installed:
- Install Postgres and create db
- Or use your favourite online postgres service if you want (you have to 
  connect your online db to API)


## 1. Clone the repository

Clone this repository to your local machine using the following command:

```
git clone https://github.com/julia4406/train-ticket-service
cd train-ticket-service
```

## 2. Set up a virtual environment (optional)

It's recommended to use a virtual environment to manage dependencies. To 
create and activate a virtual environment:

- On Windows:
```
python -m venv .venv
.venv\Scripts\activate
```

- On macOS/Linux:

```
python -m venv .venv
source .venv/bin/activate
```

## 3. Install the dependencies

Install the required Python packages from requirements.txt:

```pip install -r requirements.txt```

## 4. Set up environment variables

Make sure to create a `.env` file in the root of the project with the necessary environment variables. You can use the .env.sample file as a reference. For example:

- .env
```
SECRET_KEY=<your-secret-key>

POSTGRES_DB=<your db name> or try with example: trip_db
POSTGRES_USER=<your db username> or try with example: admin
POSTGRES_PASSWORD=<your db user password> or try with example: some_password
POSTGRES_HOST=<your db hostname> or try with example: postgres-trip

PGADMIN_DEFAULT_EMAIL=<your db name> or try with example: admin@gmail.com
PGADMIN_DEFAULT_PASSWORD=<your db name> or try with example: admin
```

## 5. Run database migrations

- Apply the database migrations to set up your database schema:

```python manage.py migrate```

- If you sad about your empty database - you can install this fixture to try API 
with demo-data:

```python manage.py loaddata fixtures.json```

- **Note:** here is default-user from fixtures (or create new one -> next step)
  - login: `admin@admin.com`
  - password: `123123`


## 6. Create a superuser (optional)

If you need to create a superuser to access the Django admin panel, run:

```python manage.py createsuperuser```

Follow the prompts to create the superuser account.

## 7. Run the app

Start the development server:

```python manage.py runserver```

The application will be available at starting endpoint [http://127.0.0.
1:8000/api/trip/](http://127.0.0.1:8000/api/trip/)

To make any actions with data - Authorize your user(to create orders) 
or admin (to do everything) go to the endpoint [http://127.0.0.
1:8000/api/user/token//](http://127.0.0.1:8000/api/user/token/)


## 8. Access the admin panel (optional)

You can log into the Django admin panel at:

[http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

Use the superuser credentials you created earlier to log in.

---
That's it! You should now have the project running locally. \
Have fun! Enjoy working on it.
