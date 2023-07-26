# Change Management Database

[Change Management Database](https://github.com/indigo-dc/cmdb) (CMDB) is a python web service for managing information about business entities. It exposes a REST API to access data stored in a [neo4j](https://neo4j.com/) graph database. The service is integrated with indigo IAM, thus all requests need to pass Bearer JWT token in the authorization header.

The [INDIGO PaaS Orchestrator](https://github.com/indigo-dc/orchestrator) interacts with this service in order to obtain the list of services, belonging to different providers, available to a specific user group and the corresponding quota assigned to it.

It is a python application based on [FastAPI](https://fastapi.tiangolo.com/); it is a fully stateless service; it can be used by several Orchestrators, or by any other REST client complying with the expected JSON request. Since it is based on FastAPI it comes up with an online documentation for the API.