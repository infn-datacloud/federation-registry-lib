from typing import List

from app.flavor.models import Flavor
from app.image.models import Image
from app.provider.models import Provider
from app.service.models import Service
from neomodel import (
    One,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrMore,
)


class UserGroup(StructuredNode):
    """User Group class.

    Node containing the user group name and a brief description.
    A UserGroup has access to a set of images and flavors. It
    has access for each provider to only one project. For each
    provider it can have a SLA defining the services and the
    resources it can access.

    Attributes:
        uid (int): UserGroup unique ID.
        description (str): Brief description.
        name (str): UserGroup name.
    """

    uid = UniqueIdProperty()
    description = StringProperty(default="")
    name = StringProperty(required=True)

    slas = RelationshipTo("..sla.models.SLA", "AGREE", cardinality=ZeroOrMore)
    identity_provider = RelationshipTo(
        "..identity_provider.models.IdentityProvider",
        "BELONG_TO",
        cardinality=One,
    )

    query_prefix = """
        MATCH (g:UserGroup)
        WHERE (id(g)=$self)
        MATCH (g)-[:AGREE]-(s)-[:REFER_TO]->(p)
        """

    def flavors(self) -> List[Flavor]:
        results, columns = self.cypher(
            f"""
                {self.query_prefix}
                MATCH (p)-[:CAN_USE_VM_FLAVOR]->(u)
                RETURN u
            """
        )
        return [Flavor.inflate(row[0]) for row in results]

    def images(self) -> List[Image]:
        results, columns = self.cypher(
            f"""
                {self.query_prefix}
                MATCH (p)-[:CAN_USE_VM_IMAGE]->(u)
                RETURN u
            """
        )
        return [Image.inflate(row[0]) for row in results]

    def providers(self) -> List[Provider]:
        results, columns = self.cypher(
            f"""
                {self.query_prefix}
                MATCH (p)<-[:BOOK_PROJECT_FOR_SLA]-(u)
                RETURN u
            """
        )
        return [Provider.inflate(row[0]) for row in results]

    def services(self, **kwargs) -> List[Service]:
        if not kwargs:
            filters = ""
        else:
            filters = []
            for k, v in kwargs.items():
                if k.startswith("service_"):
                    start_idx = len("service_")
                    attr = k[start_idx:]
                    filters.append(f"u.{attr} = ${k}")
                elif k.startswith("quota_"):
                    start_idx = len("quota_")
                    attr = k[start_idx:]
                    filters.append(f"q.{attr} = ${k}")
            filters = ", ".join(filters)
            filters = "WHERE " + filters

        results, columns = self.cypher(
            f"""
                {self.query_prefix}
                MATCH (p)-[:USE_SERVICE_WITH]->(q)-[:APPLY_TO]->(u)
                {filters}
                RETURN u
            """,
            kwargs,
        )
        return [Service.inflate(row[0]) for row in results]
