

Populating behavior


An external script, for each provider written in a configuration file, populates the database with the retrieved providers’ data. The script retrieves these data hitting specific provider endpoints or through configuration parameters hard coded in the script. If the provider does not exist the script creates it, otherwise update it with the new data.

When creating a new provider instance, the endpoint connects and eventually creates the provider’s location, identity providers, projects; the endpoints create all the projects.

When updating a provider instance, the endpoint updates existing connections with location, clusters, images, flavors, and identity providers, adds new ones or removes existing ones. For projects it updates existing ones, creates new instances if not yet connected and removes deleted projects.

If a provider is no longer inside the list, it is deleted from the database. When a cluster, flavor, image or location have no connections, they can be deleted from the database.

The same external script reads the list of users present on the IAM service and populates the database with the retrieved user groups. They can live with no connections.

SLA are manually inserted. When creating an SLA, the user must specify the user group and the project. For each service it can add a set of quotas. It should be impossible to connect a user group with a new project, belonging to a provider already connected to this user group through another SLA. The update of an existing SLA is done manually.


Users Access

When a user decides to deploy a new instance, at first, he selects one of the user groups he belongs to. This choice will be used to check the projects and the corresponding providers’ resources and SLAs it has access to.

When a user performs a request on the database, in the bearer token it specifies a user group which they belong to. All allowed user groups are mapped into the database. A user group to read or make changes to the database must belong to one of the identity providers supported by the target provider.

Then, the user selects the application he wants to use. Based on the selected operations, the deployment will use a TOSCA template to set the deployment properties. The TOSCA template node property identifies the required IaaS service type (VM, kubernetes, Storage...). Based on the required service type the dashboard retrieves information from the DB to default text fields (VM Image, VM flavor...).

When the deployment starts, based on the required service type and the SLAs assigned to the selected user groups’ projects, the orchestrator checks which quotas are allowed for any of the connected services. If an SLA does not have enough reserved resources for a specific a service, belonging to a specific provider, that provider is automatically discarded.


