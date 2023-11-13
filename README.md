# Configuration-Management-Database

The Configuration-Management-Database is a web application providing public REST API to inspect the configurations of the providers registered into the DataCloud project.

It uses a [neo4j](https://neo4j.com/) graph database to store configurations, a [FastAPI](https://fastapi.tiangolo.com/) python backend providing the public REST API and a [Next](https://nextjs.org/) frontend, based on [React](https://react.dev/), to visualize and edit the database data.

It is a [docker](https://www.docker.com/) based application.

# Installation and Usage

Clone this repository and move inside the project top folder.

```bash
git clone https://baltig.infn.it/infn-cloud/paas/catalog-api
cd catalog-api
```

To start up the service in production mode use docker compose. **It requires an external network named _traefik-public_**:

```bash
docker compose up -d
```

# Developers

> This repository makes use of githooks. To enable them install [pre-commit](https://pre-commit.com/) and run the `pre-commit install` command.

## Running

To start the service in development mode using docker compose type:

```bash
docker compose up -f docker-compose.yml -f docker-compose.override.yml up -d
```

otherwise, to start the service locally in development mode, look at the `README.md` in each subfolder.




This is a [FastAPI](https://fastapi.tiangolo.com/) project.

## Getting Started

Start the virtual environment:

```bash
poetry install
poetry shell
```

Start your neo4j database. If you want, from the top folder, you can run a dockerized version with the following command:

```bash
docker compose -f docker-compose.neo4j.dev.yml up -d
```

Finally run the development server (use the --reload flag to allow server reload on changes):

```bash
uvicorn app.main --reload
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) with your browser to see the automatic documentation. From this page you can test the API.
