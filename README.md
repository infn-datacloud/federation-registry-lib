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

## Production deployment

### Requirements

You need to have `docker` installed on your system and a running `neo4j` database instance.

In idle mode, the application uses at least 1.2 GiB of memory space and the `gunicorn` service starts 25 processes (PIDS).

A database with about 20000 entities occupies 500MB of disk space.

> These details can be retrieved running `docker stats` on the host machine and running `du -hs <path-to>/data` on the machine hosting the database.

### Start up the services

In production mode you should run the application using the dedicated image [indigopaas/federation-registry](https://hub.docker.com/r/indigopaas/federation-registry) available on DockerHub.

The command to start the application inside a container is:

```bash
docker run -p 8000:80 -d indigopaas/federation-registry
```

The previous command makes the application available on port 8000 of the host in detached mode.

The application does not requires persistent volumes.

It uses environment variables to configure the database connection, the list of trusted identity providers, the admin users and the endpoint prefix for all requests. You can pass these variables as arguments when starting the container. In the following table we list all the environment variables that can be passed to the command.

| Name                    | Mandatory | Description                                                                                                                                                                                                                                                                               | Default value                        |
| ----------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| `PROJECT_NAME`          |           | The project name that will be displayed on the online documentation.                                                                                                                                                                                                                      | Federation-Registry                  |
| `DOMAIN`                | x         | Host domain name. In production mode you should set this value equal to the domain at which your app will be available. **If you are using traefik you should re-use this value in the docker-compose labels. A default value if provided to simplify development environment start up.** | localhost:8000                       |
| `API_V1_STR`            |           | Prefix to use to execute requests on the first version of the API. If you are using a reverse-proxy you can customize this prefix based on your needs. (**Start with "/" and do not end with "/"**)                                                                                       | /api/v1                              |
| `NEOMODEL_DATABASE_URL` | x         | The complete URL to reach the neo4j database. **Although it is mandatory, if this value has not been set, the application can be build it from the `NEO4J_URI_SCHEME`, `NEO4J_USER`, `NEO4J_PASSWORD` and `NEO4J_SERVER` env variables.**                                                 | bolt://neo4j:password@localhost:7687 |
| `NEO4J_SERVER`          |           | This value defines the host and eventually the port providing the neo4j database. **It is used only if `NEOMODEL_DATABASE_URL` has not been set.**                                                                                                                                        | localhost:7687                       |
| `NEO4J_USER`            |           | This value defines the user to use to access to the database. **It is used only if `NEOMODEL_DATABASE_URL` has not been set.**                                                                                                                                                            | neo4j                                |
| `NEO4J_PASSWORD`        |           | This value defines the host and eventually the port providing the neo4j database. **It is used only if `NEOMODEL_DATABASE_URL` has not been set.**                                                                                                                                        | password                             |
| `NEO4J_URI_SCHEME`      |           | This value defines the host and eventually the port providing the neo4j database. **It is used only if `NEOMODEL_DATABASE_URL` has not been set.**                                                                                                                                        | bolt                                 |
| `MAINTAINER_NAME`       |           | Name and surname of the application maintainer. This will be shown in the automatic OpenAPI documentation.                                                                                                                                                                                | null                                 |
| `MAINTAINER_URL`        |           | Link to the application maintainer's personal home page (i.e. github). This will be shown in the automatic OpenAPI documentation.                                                                                                                                                         | null                                 |
| `MAINTAINER_EMAIL`      |           | Email of the application maintainer. This will be shown in the automatic OpenAPI documentation.                                                                                                                                                                                           | null                                 |
| `ADMIN_EMAIL_LIST`      | x         | List of emails belonging to the users authorized to perform write operations. **The project starts also if this variable is not set but write operations will fail.**                                                                                                                     | []                                   |
| `TRUSTED_IDP_LIST`      | x         | List of trusted identity providers to use to verify users' identity. **The project starts also if this variable is not set but operations requiring authentication will fail.**                                                                                                           | []                                   |

Some of these variables are not mandatory. If not specified they will use the default value.

The default values for `ADMIN_EMAIL_LIST` and `TRUSTED_IDP_LIST` are empty lists. With these values it is not possible to perform any request.

You can also create a `.env` file with all the variables you want to override. Here an example overriding all variables

```bash
# .env

PROJECT_NAME=My-Federation-Registry
DOMAIN=my.federation.registry.com
API_V1_STR=/my-fed-reg/api/v1

NEOMODEL_DATABASE_URL=bolt://neo4j:mypwdlongandlong@test.db-host.it

MAINTAINER_NAME="John"
MAINTAINER_URL="https://app-maintainer@github.com/"
MAINTAINER_EMAIL="test@support.it"

TRUSTED_IDP_LIST=["https://test.idp.it"]
ADMIN_EMAIL_LIST=["test@admin-user.it"]
```

Alternative example using the `NEO4J_` env variables:

```bash
# .env

PROJECT_NAME=My-Federation-Registry
DOMAIN=my.federation.registry.com
API_V1_STR=/my-fed-reg/api/v1

NEO4J_SERVER=test.db-host.it
NEO4J_USER=neo4j
NEO4J_PASSWORD=mypwdlongandlong
NEO4J_URI_SCHEME=bolt

MAINTAINER_NAME="John"
MAINTAINER_URL="https://app-maintainer@github.com/"
MAINTAINER_EMAIL="test@support.it"

TRUSTED_IDP_LIST=["https://test.idp.it"]
ADMIN_EMAIL_LIST=["test@admin-user.it"]
```

### Ancillary services

To correctly work, the application requires a running neo4j database instance with the **apoc** extension.

If you don't have an already running instance, we suggest to deploy your instance using the [neo4j](https://hub.docker.com/_/neo4j) docker image available on DockerHub and make persistent the `/data` and `/logs` volumes.

> To enable apoc extensions, when creating the instance pass the following environment variable: `NEO4J_PLUGINS=["apoc"]`

# Developers

## Setting up environment

Developers can launch the project locally or using containers. In both cases, developers need a running **neo4j database** and an **oidc-agent service**. These two services can be started in containers.

### Local Development (suggested for Linux users)

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

### VSCode Dev-Container (suggested for MacOS users)

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

> Warning for Linux users who want to use devcontainer: when creating or editing a file inside the container, that file will belong to the root user. This way, you must be super-user to edit that file outside the container.

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
