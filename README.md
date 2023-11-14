# Federation Registry

The Federation Registry is a web application providing public REST API to inspect the configurations of the providers registered into the DataCloud project. It is one of the microservices used by the orchestrator.

It uses a [neo4j](https://neo4j.com/) graph database to store configurations and a [FastAPI](https://fastapi.tiangolo.com/) python backend providing the public REST API. Authentication is made using token. These tokens can be generated using [oidc-agent](https://indigo-dc.gitbook.io/oidc-agent/).

It is a [docker](https://www.docker.com/) based application.

# Installation and Usage

## Download the project

Clone this repository and move inside the project top folder.

```bash
git clone https://github.com/indigo-paas/federation-registry.git
cd federation-registry
```

## Start up the services

**TODO: Define how to start the service in production mode.**

# Developers

## Setting up environment

Developers can launch the project locally or using containers. In both cases, developers need a running **neo4j database** and an **oidc-agent service**. These two services can be started in containers.

### Local Development

Requirements:

- Docker (to start services)
- Poetry

If you don't have an already running instance, we suggest to start the **neo4j database** and the **oidc-agent service** using the docker-compose files provided in this repository. The docker-compose is located inside the `.devcontainer` folder. So move into this folder and start the compose services.

```bash
cd .devcontainer
docker compose up -d db oidc-agent
```

Then, using [poetry](https://python-poetry.org/), developers can install the libraries needed to start the python app and the tools to manage the code versioning, linting and formatting.

```bash
poetry install
poetry shell
```

### VSCode Dev-Container

Requirements:

- Docker

Using VSCode you can open the entire folder inside the provided container. The docker-compose, located in the `.devcontainer` folder, starts the **neo4j database**, the **oidc-agent service** and a python based container with all the needed libraries and tool already installed.

> The _docker-outside-docker_ extension allows developers to connect to the docker daemon service running on their host from inside the container.

> If you are using `docker compose` instead of `docker-compose`. Verify that in the VSCode User Settings `Dev › Containers: Docker Compose Path` you are using **docker compose** instead of **docker-compose**.

### Start up the app

To run the application in development mode developers can use the following command(the --reload flag allows server reload on changes):

```bash
uvicorn app.main --reload
```

### Browser access

Once the web server is ready, at [http://localhost:8000/docs](http://localhost:8000/docs) developers can see the automatic documentation produced by FastAPI. From this page they can manually test the API.

If you started the neo4j database using the docker-compose provided in this repository, the neo4j database can be accessed at [http://localhost:7474/browser/](http://localhost:7474/browser/).

> In development mode no username and password are needed.

### Tools

This repository makes use of githooks such as [pre-commit](https://pre-commit.com/). This tools is configured to prevent to commit code with syntax errors or not well formatted.

Tests have been developed using [pytest](https://docs.pytest.org/en/latest/). Coverage configuration details are defined in the `.coveragerc` file.

Formatting and linting is made through [ruff](https://docs.astral.sh/ruff/). Ruff configuration is defined in the `pyproject.toml` file and the `pre-commit` githook runs the linting on the code. The linting and the formatting can be manually launched on the project. Look at the online documentation for the commands syntax.

To run locally the github actions developers can use [act](https://github.com/nektos/act).

> In order for the **test-analysis** job to work, users must define locally the **SONAR_TOKEN** env variable.
