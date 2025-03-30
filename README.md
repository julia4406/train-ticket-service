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

  - main service via api/trips/
  - user actions(create, access token, profile) via api/users/
  - documentation:
    -  swagger api/doc/swagger/
    -  redoc api/doc/redoc/

## Other notes about version 1.0.0:
- trains consists of carriages of one type only
- tickets can be created and viewed through ORDER-endpoint only
- PAGINATION 
    - off by default
    - pagination can be controlled using query parameters
    - The `limit` and `offset` parameters allow adjusting the response size and starting position
      - **Example**
      - `GET /trips/` → returns all items
      - `GET /trips/?limit=10` → returns 10 items per page
      - `GET /trips/?limit=5&offset=15` → returns 5 items starting 
        from 16th
- Search and filtering available on all endpoints. See documentation: `swagger api/doc/swagger/`
- Ticket validation includes:
    - Impossible to book one seat twice (prevents double booking)
- Trip date validation (arrival time cannot be earlier than departure time)
- *Orders:*
  - for users: allowed only orders from this account
  - for administrators: all orders can be viewed
- Configured to show quantity of seats:
  - in list view: total available in train for trip
  - in detail view: seats booked, total seats capacity, seats available(free)


****
# 🔧 Setup and launch

### Installing using GitHub:
****
 
- [**SETUP**](SETUP.md)


### Run with docker:
****

- ***Docker should be installed!***
- Download image [https://hub.docker.com/repository/docker/julia4406/train_ticket_service_api_drf/](https://hub.docker.com/repository/docker/julia4406/train_ticket_service_api_drf/general)

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

- create user via /api/users/register/
- get access token via /api/users/token/
- starting endpoint via /api/trips/trips/

