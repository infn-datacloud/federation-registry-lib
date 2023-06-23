from neomodel import StringProperty, StructuredRel


class BookProject(StructuredRel):
    """Relationship linking a Project to a Provider.

    Attributes:
        name (str): Name of the Project in the Provider.
        uuid (uuid): Project Unique ID in the Provider.
    """

    name = StringProperty(required=True)
    uuid = StringProperty(required=True)
