
I build this as a monoltih app as a Django project

there are two apps

- website (website frontend)
- api (backend of the application and rest framework)

## Development

```
cd app
docker-compose up -d --build
```

### Load Fixtures

```
docker-compose exec budgets python manage.py loaddata budgets.json
```


### Run Tests

```
docker-compose exec budgets
```
#### Run tests with coverage report
```
docker-compose exec budgets pytest -p no:warnings --cov=. --cov-report html
```

### Code formatting
```
docker-compose exec budgets black --exclude=migrations .
docker-compose exec budgets isort .
docker-compose exec budgets flake8 .
```


### Using the app

To test the app go to http://localhost:8009/

You can login with this credentials for the test user

```
username: test@email.com
password: Password123$
```

You can see the api documentaction on http://localhost:8009/swagger-docs/