# Federation Registry

The Federation Registry is a web application providing public REST API to inspect the configurations of the federated providers of the DataCloud project. It is one of the microservices used by the orchestrator.

It uses a [neo4j](https://neo4j.com/) graph database to store configurations and a [FastAPI](https://fastapi.tiangolo.com/) python backend providing the public REST API. The [flaat](https://github.com/indigo-dc/flaat) module manages authentication and authorizations over all the application endpoints. User authentication can be done using tokens generated by [oidc-agent](https://indigo-dc.gitbook.io/oidc-agent/). In production mode the application is meant to be used with [docker](https://www.docker.com/).

# Application logic

All write endpoints (DELETE, PATCH, POST and PUT) have a strict security: If a user is not authenticated or does not have the write access rights, the endpoints raise a 401 or 403 error. On the other hand read endpoints use a lazy security: If a user is not authenticated, they can see a shrunk version of the data, whereas authenticated users can choose to see the whole data or a the shrunk version. Failed authentication (invalid token) will return a 403 error also for read endpoints.

Each database entity has a set of endpoints. All endpoints starts with a prefix which can be defined by the user (see `API_V1_STR` environment variable).

Here a list of the entities (and related endpoints):

- `Flavor`:
  - **endpoint**: `/flavors/`
  - **methods**: `DELETE` (single), `GET` (single and multiple) and `PATCH` (single)
- `Identity Provider`:
  - **endpoint**: `identity_providers`
  - **methods**: `DELETE` (single), `GET` (single and multiple) and `PATCH` (single)
- `Image`:
  - **endpoint**: `images`
  - **methods**: `DELETE` (single), `GET` (single and multiple) and `PATCH` (single)
- `Location`:
  - **endpoint**: `locations`
  - **methods**: `DELETE` (single), `GET` (single and multiple) and `PATCH` (single)
- `Network`:
  - **endpoint**: `networks`
  - **methods**: `DELETE` (single), `GET` (single and multiple) and `PATCH` (single)
- `Project`:
  - **endpoint**: `projects`
  - **methods**: `DELETE` (single), `GET` (single and multiple) and `PATCH` (single)
- `Provider`:
  - **endpoint**: `providers`
  - **methods**: `DELETE` (single), `GET` (single and multiple), `PATCH` (single), `POST` (single) and `PUT` (single)
- `Block Storage Quota`:
  - **endpoint**: `block_storage_quotas`
  - **methods**: `DELETE` (single), `GET` (single and multiple) and `PATCH` (single)
- `Compute Quota`:
  - **endpoint**: `compute_quotas`
  - **methods**: `DELETE` (single), `GET` (single and multiple) and `PATCH` (single)
- `Network Quota`:
  - **endpoint**: `network_quotas`
  - **methods**: `DELETE` (single), `GET` (single and multiple) and `PATCH` (single)
- `Region`:
  - **endpoint**: `regions`
  - **methods**: `DELETE` (single), `GET` (single and multiple) and `PATCH` (single)
- `Block Storage Service`:
  - **endpoint**: `block_storage_services`
  - **methods**: `DELETE` (single), `GET` (single and multiple) and `PATCH` (single)
- `Compute Service`:
  - **endpoint**: `compute_services`
  - **methods**: `DELETE` (single), `GET` (single and multiple) and `PATCH` (single)
- `identity Service`:
  - **endpoint**: `identity_services`
  - **methods**: `DELETE` (single), `GET` (single and multiple) and `PATCH` (single)
- `Network Service`:
  - **endpoint**: `network_services`
  - **methods**: `DELETE` (single), `GET` (single and multiple) and `PATCH` (single)
- `SLA (Service Level Agreement)`
  - **endpoint**:`slas`
  - **methods**: `DELETE` (single), `GET` (single and multiple) and `PATCH` (single)
- `User Group`
  - **endpoint**:`user_groups`
  - **methods**: `DELETE` (single), `GET` (single and multiple) and `PATCH` (single)

# Production deployment

## Requirements

You need to have `docker` installed on your system and a running `neo4j` database instance.

In idle mode, the application uses at least 1.2 GiB of memory space and the `gunicorn` service starts 25 processes (PIDS).

A database with about 20000 entities occupies 500MB of disk space.

> These details can be retrieved running `docker stats` on the host machine and running `du -hs <path-to>/data` on the machine hosting the database.

## Start up the services

In production mode you should run the application using the dedicated image [indigopaas/federation-registry](https://hub.docker.com/r/indigopaas/federation-registry) available on DockerHub.

The application **does not requires persistent volumes**.

On the other hand, it uses **environment variables** to configure the database connection, the list of trusted identity providers, the admin users and the endpoint prefix for all requests. You can pass these variables as arguments when starting the container.

The command to correctly start up the application inside a container using the environment variables default is:

```bash
docker run -p 8000:80 -d indigopaas/federation-registry
```

The previous command makes the application available on port 8000 of the host in detached mode. Moreover the application will try to connect to a neo4j instance located at bolt://neo4j:password@localhost:7687. Unfortunately, operations requiring authentication or authorizations will fail since no trusted issuers and admin users have been set.

In the following table we list all the environment variables that can be passed to the command using the `-e` param.

- `ADMIN_EMAIL_LIST`
  - **description**: List of emails belonging to the users authorized to perform write operations.
  - **type**: list of email
  - **mandatory**: YES. **The project starts also if this variable is not set but write operations will fail.**
  - **default**: []. _A default value if provided only to simplify development environment start up._
- `TRUSTED_IDP_LIST`
  - **description**: List of trusted identity providers to use to verify users' identity.
  - **type**: list of URL
  - **mandatory**: YES. **The project starts also if this variable is not set but operations requiring authentication will fail.**
  - **default**: []. _A default value if provided only to simplify development environment start up._
- `DOMAIN`
  - **description**: Host domain name. In production mode you should set this value equal to the domain at which your app will be available. Omit uri scheme (http, https...). If you are using a specific port you can add it to this variable. **If you are using traefik you should re-use this value in the docker-compose labels.**
  - **type**: string
  - **mandatory**: YES
  - **default**: localhost:8000. _A default value if provided only to simplify development environment start up._
- `NEO4J_DB_URL`
  - **description**: The complete URL to reach the `neo4j` database instance.
  - **type**: url
  - **mandatory** YES. **Alternatively, if this value has not been set, the application can build it from the `NEO4J_URI_SCHEME`, `NEO4J_USER`, `NEO4J_PASSWORD` and `NEO4J_SERVER` env variables.**
  - **default**: None. _It is build from `NEO4J_URI_SCHEME`, `NEO4J_USER`, `NEO4J_PASSWORD` and `NEO4J_SERVER` env variables._
- `NEO4J_SERVER`:
  - **description**: This value defines the host and eventually the port providing the `neo4j` database instance. **It is used only if `NEO4J_DB_URL` has not been set.**
  - **type**: string
  - **mandatory**: NO. _See `NEO4J_DB_URL` to understand when it is mandatory._
  - **default**: localhost:7687. _A default value if provided only to simplify development environment start up._
- `NEO4J_USER`
  - **description**: This value defines the user to use to access to the `neo4j` database instance. **It is used only if `NEO4J_DB_URL` has not been set.**
  - **type**: string
  - **mandatory**: NO. _See `NEO4J_DB_URL` to understand when it is mandatory._
  - **default**: neo4j. _A default value if provided only to simplify development environment start up._
- `NEO4J_PASSWORD`
  - **description**: This value defines the host and eventually the port providing the `neo4j` database instance. **It is used only if `NEO4J_DB_URL` has not been set.**
  - **type**: string
  - **mandatory**: NO. _See `NEO4J_DB_URL` to understand when it is mandatory._
  - **default**: password. _A default value if provided only to simplify development environment start up._
- `NEO4J_URI_SCHEME`
  - **description**: This value defines the host and eventually the port providing the `neo4j` database instance. **It is used only if `NEO4J_DB_URL` has not been set.**
  - **type**: One of `bolt`, `bolt+s`, `neo4j` or `neo4j+s`
  - **mandatory**: NO. _See `NEO4J_DB_URL` to understand when it is mandatory._
  - **default**: bolt. _A default value if provided only to simplify development environment start up._
- `PROJECT_NAME`
  - **description**: The project name that will be displayed on the online documentation.
  - **type**: string
  - **mandatory**: NO
  - **default**: Federation-Registry
- `API_V1_STR`
  - **description**: Prefix to use to execute requests on the first version of the API. If you are using a reverse-proxy you can customize this prefix based on your needs.
  - **type**: string starting with `/`.
  - **mandatory**: NO
  - **default**: /api/v1
- `MAINTAINER_NAME`:
  - **description**: Name and surname of the application maintainer. This will be shown in the automatic OpenAPI documentation.
  - **type**: string
  - **mandatory**: NO
  - **default**: null
- `MAINTAINER_URL`:
  - **description**: Link to the application maintainer's personal home page (i.e. github). This will be shown in the automatic OpenAPI documentation.
  - **type**: string
  - **mandatory**: NO
  - **default**: null
- `MAINTAINER_EMAIL`:
  - **description**: Email of the application maintainer. This will be shown in the automatic OpenAPI documentation.
  - **type**: email
  - **mandatory**: NO
  - **default**: null

> The default values for `ADMIN_EMAIL_LIST` and `TRUSTED_IDP_LIST` are empty lists. With these values it is not possible to perform any request.

You can also create a `.env` file with all the variables you want to override. Here an example:

```bash
# .env

PROJECT_NAME=My-Federation-Registry
DOMAIN=my.federation.registry.com
API_V1_STR=/my-fed-reg/api/v1

NEO4J_DB_URL=bolt://neo4j:mypwdlongandlong@test.db-host.it

MAINTAINER_NAME=John
MAINTAINER_URL=https://app-maintainer@github.com/
MAINTAINER_EMAIL=test@support.it

TRUSTED_IDP_LIST=["https://test.idp.it"]
ADMIN_EMAIL_LIST=["test@admin-user.it"]
```

Alternative example using the `NEO4J_` single env variables:

```bash
# .env

PROJECT_NAME=My-Federation-Registry
DOMAIN=my.federation.registry.com
API_V1_STR=/my-fed-reg/api/v1

NEO4J_SERVER=test.db-host.it
NEO4J_USER=neo4j
NEO4J_PASSWORD=mypwdlongandlong
NEO4J_URI_SCHEME=bolt

MAINTAINER_NAME=John
MAINTAINER_URL=https://app-maintainer@github.com/
MAINTAINER_EMAIL=test@support.it

TRUSTED_IDP_LIST=["https://test.idp.it"]
ADMIN_EMAIL_LIST=["test@admin-user.it"]
```

## Ancillary services

To correctly work, the application requires a running neo4j database instance with the **apoc** extension.

If you don't have an already running instance, we suggest to deploy your instance using the [neo4j](https://hub.docker.com/_/neo4j) docker image available on DockerHub and make persistent the `/data` and `/logs` volumes.

> To enable apoc extensions, when creating the instance pass the following environment variable: `NEO4J_PLUGINS=["apoc"]`

# Developers

## Installation

Clone this repository and move inside the project top folder.

```bash
git clone https://github.com/indigo-paas/federation-registry.git
cd federation-registry
```

## Setting up environment

Developers can launch the project locally or using containers.

In both cases, developers need a running `neo4j` database which can be started using docker.

Optionally they can have an `oidc-agent` service which will be useful to generate the token to use to perform authenticated read and write operations. Again this can be started using docker.

### Local Development (suggested for Linux users)

Requirements:

- Docker (to start `neo4j` and `oidc-agent` services)
- Poetry

If you don't have an already running instance, we suggest to start the `neo4j` database and the optional `oidc-agent` service using the `docker-compose.yml` is located inside the `.devcontainer` folder.

```bash
cd .devcontainer
docker compose up -d db [oidc-agent]
```

or

```bash
docker compose -f .devcontainer/docker-compose.ymal up -d db [oidc-agent]
```

Then, using [poetry](https://python-poetry.org/), developers can install the libraries needed to start the python app and the tools to manage the code versioning, linting and formatting.

We suggest to configure poetry to create the virtual environment inside the project folder to help VSCode environment discover.

```bash
poetry config virtualenvs.in-project true
poetry install
```

The previous commands should be execute just the first time. You shall run the install step again when downloading a newer version of the project.

To activate the virtual environment you can run the following command:

```bash
poetry shell
```

### VSCode Dev-Container (suggested for MacOS users)

Requirements:

- Docker

Using VSCode you can open the entire folder inside the provided development container. The `docker-compose.yaml`, located in the `.devcontainer` folder, starts a `neo4j` database, an `oidc-agent` service and a python based container with all the production and development libraries. The development container use a non root user **vscode** with sudoers privileges, it has access to the host docker service and has a set of VSCode extensions already installed.

> The _docker-outside-docker_ extension allows developers to connect to the docker daemon service running on their host from inside the container.

> If you are using `docker compose` instead of `docker-compose`. Verify that in the VSCode User Settings `Dev › Containers: Docker Compose Path` you are using **docker compose** instead of **docker-compose**.

## Start up the app

To run the application in development mode developers can use the following command(the --reload flag allows server reload on changes):

```bash
uvicorn app.main --reload
```

Alternatively, users using VSCode, can use the `launch.json` file provided in the `.vscode` folder to run the application. The `Uvicorn: FastAPI app` configuration will execute the previous command.

## Browser access

Once the web server is ready, at [http://localhost:8000/docs](http://localhost:8000/docs) developers can see the automatic documentation produced by FastAPI. From this page they can manually test the API.

If you started the neo4j database using the docker-compose provided in this repository, the neo4j database can be accessed at [http://localhost:7474/browser/](http://localhost:7474/browser/).

> In development mode no username and password are needed.

## Testing

### Manual tests

At first, once you have a running instance of the application (both the python backend and the neo4j database), you should try to execute a GET requests using `curl` (without authentication) on any of the provided endpoint. Instead of `curl` you can use `postman`.

```bash
curl -X GET http://localhost:8000/api/v1/providers/
```

The first time you should receive as response an empty list `[]` since no entries have been added to the database

Then you can try to add a new instance to the database using a POST request. To do this you must have a valid authentication token and send a valid json dict. As previously said the only POST endpoint is the providers' one.

```bash
curl -X POST http://localhost:8000/api/v1/providers/ \
    -H 'Authorization: Bearer <token>' \
    -H 'Content-Type: application/json' \
    -d '{ "name": "test", "type": "openstack"}'
```

As response you will receive a dict with the provider data you just added:

```json
{
  "description": "",
  "name": "test",
  "type": "openstack",
  "status": "active",
  "is_public": false,
  "support_emails": [],
  "uid": "e442d95782314760bd78bbcf78c863a0",
  "identity_providers": [],
  "projects": [],
  "regions": []
}
```

Finally, you can retry the GET request without authentication or with authentication. In the first case you will receive a shrunk version of the data.

Take a look at the [automatic online documentation](http://localhost:8000/docs) to have a full list of the possible parameters and to try different requests.

### Automatic tests

Automatic tests have been implemented using the `pytest` and `pytest-cases` library.

To run the test suite you can run, from the project top folder, the following command:

```bash
pytest
```

## Tools

This repository makes use of githooks such as [pre-commit](https://pre-commit.com/). This tools is configured to prevent to commit code with syntax errors or not well formatted.

Tests have been developed using [pytest](https://docs.pytest.org/en/latest/) and [pytest-cases](https://smarie.github.io/python-pytest-cases/). Coverage configuration details are defined in the `.coveragerc` file.

Formatting and linting is made through [ruff](https://docs.astral.sh/ruff/). Ruff configuration is defined in the `pyproject.toml` file and the `pre-commit` githook runs the linting and formatting on the code. The linting and the formatting can be manually launched on the project. Look at the online documentation for the commands syntax.

To run locally the github actions developers can use [act](https://github.com/nektos/act).

> In order for the **test-analysis** job to work, users must define locally the **SONAR_TOKEN** env variable.

## Build the image

A github action build and push a new docker image version on dockerhub with the name [indigopaas/federation-registry](https://hub.docker.com/r/indigopaas/federation-registry) on each push or merge on the main branch. To have a local build on your PC you can run this command:

```bash
docker build -t indigopaas/federation-registry .
```
