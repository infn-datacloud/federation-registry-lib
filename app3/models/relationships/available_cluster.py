from neomodel import StringProperty, StructuredRel


class AvailableCluster(StructuredRel):
    """Supported Cluster class.

    Relationship linking a flavor to the provider
    supporting it.

    Attributes:
        uid (uuid): SupportedCluster unique ID.
        flavor_name (str): Name given to the Cluster
            by the Provider.
        flavor_id (uuid): Cluster Unique ID in the Provider.
    """

    name = StringProperty(unique_index=True, required=True)
    uuid = StringProperty(unique_index=True, required=True)
