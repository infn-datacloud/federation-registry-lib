# Federation Registry Library

The Federation Registry is a web application providing public REST API to inspect the configurations of the federated providers of the DataCloud project and save them in a [neo4j](https://neo4j.com/) graph database. It is one of the microservices used by the orchestrator.

This projects contains the definition of the [pydantic](https://docs.pydantic.dev/1.10/) and [neomodel](https://neomodel.readthedocs.io/en/latest/index.html) objects used by the federation-registry. This library can be used by any client script to easily build data that will be sent to the service endpoint.

# Developers

## Tools

This repository makes use of githooks such as [pre-commit](https://pre-commit.com/). This tools is configured to prevent to commit code with syntax errors or not well formatted.

Formatting and linting is made through [ruff](https://docs.astral.sh/ruff/). Ruff configuration is defined in the `pyproject.toml` file. The linting and the formatting can be manually launched on the project. Look at the online documentation for the commands syntax.

Tests have been developed using [pytest](https://docs.pytest.org/en/latest/) and [pytest-cases](https://smarie.github.io/python-pytest-cases/). Coverage configuration details are defined in the `pyproject.toml` file.

## Installation

Clone this repository and move inside the project top folder.

```bash
git clone https://github.com/infn-datacloud/federation-registry-lib.git
cd federation-registry-lib
```

## Local Development (suggested for Linux users)

Requirements:
- Poetry
- Pre-commit

Using [poetry](https://python-poetry.org/), developers can install the needed libraries and the tools to manage the code versioning, linting and formatting.

```bash
poetry install
```

> The repository is already configured to create the virtual environment inside the project folder to help VSCode environment discover.

> The previous commands should be execute:
> - the first time to create the virtual environemnt
> - when downloading a newer version of the project with updated dependencies.

To activate the virtual environment you can run the following command:

```bash
poetry shell
```

> VSCode, configured the first time, is able to automatically load the virtual environment everytime you open the project.

To enable automatic code format check, the first time you clone the repository, you must initialize pre-commit

```bash
pre-commit init
```

## VSCode Dev-Container (suggested for MacOS users)

Requirements:

- Docker

Using VSCode you can open the entire folder inside the provided development container. The development container use a non root user **vscode** with sudoers privileges, it has access to the host docker service and has a set of VSCode extensions already installed.

> The _docker-outside-docker_ extension allows developers to connect to the docker daemon service running on their host from inside the container.

## Testing

### Start up a Neo4j DB

To correctly work, the application requires a running neo4j database instance with the **apoc** extension.

If you don't have an already running instance, we suggest to deploy your instance using the [neo4j](https://hub.docker.com/_/neo4j) docker image available on DockerHub.

In the repository we already provide a docker compose with a basic neo4j instance with the *apoc* plugin. Just run from the top folder:

```bash
docker compose -f compose.neo4j.dev.yaml up -d
```

### Automatic tests

Automatic tests have been implemented using the `pytest` and `pytest-cases` library.

To run the test suite, from the project top folder, execute the following command:

```bash
pytest
```

To show the code coverage run:

```bash
pytest --cov
```

The coverage configuration is written in the `pyproject.toml` file.

> You have correctly configured VSCode, you can also use the **Testing** plugin.
