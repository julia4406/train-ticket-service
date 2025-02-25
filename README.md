# Ticket Service API
API service for management tickets ordering from railway company written on DRF
****



# Features

- JWT Authenticated
- Admin panel /admin
- Documentation is located at api/doc/swagger/ and api/doc/redoc/
- Managing orders and tickets for authenticated users
- Viewing and filtering functions in all endpoints (for authenticated users)
- All CRUD operations allowed only for admins (is_staff=1)

## Endpoints:

  - main service via api/trip/
  - user actions(create, access token, profile) via api/user/
  - documentation:
    -  swagger api/doc/swagger/
    -  redoc api/doc/redoc/


****
# 🔧 Setup and launch

### Installing using GitHub:
****
 
- [**SETUP**](SETUP.md)


### Run with docker:
****

- ***Docker should be installed!***
- Download image [https://hub.docker.com/u/julia4406](https://hub.docker.com/u/julia4406)

```
docker-compose build
docker-compose up
```

- If you sad about your empty database - you can install this fixture to try API 
with demo-data:

```docker compose exec web python manage.py loaddata fixtures.json```

- **Note:** here is default-user from fixtures (or create new one -> next step)
  - login: `admin@admin.com`
  - password: `123123`
  

- If you need to create a superuser to access the Django admin panel, run:
```docker compose exec web python manage.py createsuperuser```


## Getting access:
****

- create user via /api/user/register/
- get access token via /api/user/token/
- starting endpoint via /api/trip/trips/

