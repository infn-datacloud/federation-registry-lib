from neomodel import (
    StringProperty,
    StructuredRel,
)


class Project(StructuredRel):
    """Associated Project class.

    Relationship linking a user group to a provider.
    This link correspond to a "project/tenant" entity.

    Attributes:
        uid (uuid): AssociatedProject unique ID.
        project_name (str): Name of the project in the
            Provider to which this UserGroup has access.
        project_id (uuid): Project Unique ID in the Provider.
        public_network_name (str): #TODO
        private_network_name (str): #TODO
        private_network_proxy_name (str): #TODO
        private_network_proxy_host (str): #TODO
    """

    project_name = StringProperty(unique_index=True, required=True)
    project_uuid = StringProperty(unique_index=True, required=True)
    public_network_name = StringProperty()
    private_network_name = StringProperty()
    private_network_proxy_host = StringProperty()
    private_network_proxy_user = StringProperty()
