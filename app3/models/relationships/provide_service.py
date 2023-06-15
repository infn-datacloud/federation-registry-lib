from neomodel import StringProperty, StructuredRel


class ProvideService(StructuredRel):
    """Associated Project class.

    Relationship linking a user group to a provider.
    This link correspond to a "project/tenant" entity.

    Attributes:
        endpoint (str): Service endpoint in the provider.
    """

    endpoint = StringProperty(unique_index=True, required=True)
