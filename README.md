# Federation Registry

The Federation Registry is a web application providing public REST API to inspect the configurations of the providers registered into the DataCloud project. It is one of the microservices used by the orchestrator.

It uses a [neo4j](https://neo4j.com/) graph database to store configurations and a [FastAPI](https://fastapi.tiangolo.com/) python backend providing the public REST API.

It is a [docker](https://www.docker.com/) based application.

# Installation and Usage

Clone this repository and move inside the project top folder.

```bash
git clone https://github.com/indigo-paas/federation-registry.git
cd federation-registry
```

## Requirements

- Docker
