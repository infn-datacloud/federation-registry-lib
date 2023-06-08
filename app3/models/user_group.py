from neomodel import (
    RelationshipTo,
    StringProperty,
    StructuredNode,
    StructuredRel,
    UniqueIdProperty,
    ZeroOrMore,
)


class AssociatedProject(StructuredRel):
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

    uid = UniqueIdProperty()
    project_name = StringProperty(required=True)
    project_id = StringProperty(required=True)
    public_network_name = StringProperty()
    private_network_name = StringProperty()
    private_network_proxy_host = StringProperty()
    private_network_proxy_user = StringProperty()


class UserGroup(StructuredNode):
    """User Group class.

    Node containing the user group name and a brief description.
    A UserGroup has access to a set of images and flavors. It
    has access for each provider to only one project. For each
    provider it can have a SLA defining the services and the
    resources it can access.

    Attributes:
        uid (uuid): UserGroup unique ID.
        name (str): UserGroup name.
        description (str): Brief description.
    """

    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    description = StringProperty(default="")

    projects = RelationshipTo(
        ".Provider",
        "ASSOCIATED_PROJECT_ON",
        cardinality=ZeroOrMore,
        model=AssociatedProject,
    )
    flavors = RelationshipTo(
        ".Flavor", "AVAILABLE_VM_SIZE", cardinality=ZeroOrMore
    )
    images = RelationshipTo(
        ".Image", "AVAILABLE_VM_IMAGE", cardinality=ZeroOrMore
    )
    slas = RelationshipTo(".SLA", "REQUIRES_RESOURCES", cardinality=ZeroOrMore)
