from neomodel import StringProperty, StructuredRel


class AvailableCluster(StructuredRel):
    """Relationship linking a VM Cluster to a Provider.

    Attributes:
        name (str): Name of the Cluster in the Provider.
        uuid (uuid): Cluster Unique ID in the Provider.
    """

    name = StringProperty(required=True)
    uuid = StringProperty(required=True)
