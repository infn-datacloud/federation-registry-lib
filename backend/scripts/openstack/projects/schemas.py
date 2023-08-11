from pydantic import UUID4, Field
from typing import Optional

from scripts.openstack.schemas import OpenstackItem


class Project(OpenstackItem):
    enabled: bool = Field(description="Item is enabled")
    is_domain: bool = Field(
        description="Indicates whether the project also acts as a domain"
    )
    domain_id: str = Field(description="Unique ID of the project domain")
    parent_id: Optional[UUID4] = Field(
        description="Unique ID of the parent project"
    )
