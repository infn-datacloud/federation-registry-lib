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

To start up the service in production mode use docker compose:

```bash
docker compose up -d
```

To start the service in development mode using docker compose type:

```bash
docker compose up -f docker-compose.yml -f docker-compose.override.yml up -d
```

otherwise, to start the service locally in development mode, look at the README.md in each subfolder.