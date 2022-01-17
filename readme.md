# Mi Águila Code Challenge

Develop a microservice-based application with two microservices that receives a CSV file and makes the appropriate calls
to the post codes (external) API

## Development

This project uses Docker, Compose and Django.

It doesn't follow Gitflow because of time constraints, but it does follow the focused commits convention


## Database

We use a simple Sqlite3 database for simplicity. For testing purposes the database is available from outside of the
container via a mounted volume that creates a database in the main application's location i.e. api/django_api/db

## Tests

Run tests using the invoke command `test`

```bash
invoke test
```

Or by starting the appropriate docker compose service

```bash
docker-compose run --rm api python manage.py test
```

## Manual testing

You can leverage the included http samples from each microservice to manually test some aspects of the application. For
example the `post_csv.http` file in api/http contains an example multipart form that POSTs the CSV file to test the 
`api/request_postcodes_from_csv` endpoint.

## Deployment
This project requires [invoke](https://www.pyinvoke.org/) to run, you can install it using pip:

```bash
pip install -U --user invoke
```


To deploy the application simply run:

```bash
invoke deploy
```
