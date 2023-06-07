from neomodel import (
    StructuredNode,
    UniqueIdProperty,
    StringProperty,
    BooleanProperty,
    RelationshipTo,
    One,
    ZeroOrMore,
)


class Service(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    resource_type = StringProperty(required=True)
    site_name = StringProperty(required=True)
    hostname = StringProperty(required=True)
    endpoint = StringProperty(required=True)
    idp_protocol = StringProperty(required=True)
    iam_enabled = BooleanProperty(default=False)

    sla = RelationshipTo(".SLA", "MANAGES_RES_ASSIGNED_TO", cardinality=One)
    idps = RelationshipTo(
        ".IdentityProvider", "AUTHENTICATES_THROUGH", cardinality=ZeroOrMore
    )
