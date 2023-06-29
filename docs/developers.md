# Developers

Here some guidelines about how to run the app, the tests suite and the style guidelines.

## Run on localhost

To run locally the python program you need [poetry](https://python-poetry.org/) installed on your system.

Use `poetry` to install dependencies and start a virtual environment with the installed dependencies:

```
poetry install
poetry shell
```

Use `uvicorn` to launch the FastAPI application. To reload the application when code changes, add the `--reload` arguments.

```
uvicorn app.main:app --reload
```

The app will be accessible to the standard url `http://localhost:8000`.

The neo4j graph database can be instantiated using the `docker-compose.neo4j.dev.yml` file. It instantiates a neo4j instance with no authentication and with apoc plugin (mandatory to use UUID in neo4j). Do not use it in production. The command to run it is:

## Run in containers

To run the python program in containers you need [docker](https://www.docker.com/) installed on your system.

If for some reason the on-line image is not available, you can build your local image issuing, from the top folder, the command:

```
docker build -t indigo-dc/poetry-fastapi -f docker/Dockerfile .
```

If you want to run a single instance of this application, and automatically remove it at the end, you can use the following command:

```
docker run --rm -it indigo-dc/poetry-fastapi
```

To run the app using `compose` see [Run the Change Management Database](getting_started.md).

## Testing the server

Tests are implemented using `pytest` module.

To run the tests, type from the main directory:

```
pytest
```

If you want to run a single test file:

```
pytest app/tests/<test_file_name>
```

If you want to see the coverage here is the command. The `--cov-report=term:missing` arguments allow you to see the lines missed by the tests:

```
pytest --cov --cov-report=term:missing
```

### Nox

To test the application over different python versions we use `nox`. To use it you need to have [conda](https://docs.conda.io/en/latest/) installed on your system.

To run it, type from the top directory:

```
nox
```

## Styling

Since we have CI/CD pipelines checking the code style, we suggest to run check the code style before perform a merge request.

Use `black` to fix formatting. Run this command from top directory:

```
black --line-length=79 .
```

Use `flake8` to check syntax and linting problems:

```
flake8 .
```

## Documentation

The documentation has been written using `mkdocs`. To run in development mode on your host the documentation use the following command:

```
mkdocs serve
```

Use the `-a` parameters to eventually change the IP and the port used by this service.
