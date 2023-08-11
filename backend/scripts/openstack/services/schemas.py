from pydantic import AnyHttpUrl, BaseModel, Field
from typing import Optional

from scripts.openstack.schemas import OpenstackItem


class Endpoints(BaseModel):
    public_endpoint: AnyHttpUrl = Field(description="Public service endpoint")
    internal_endpoint: AnyHttpUrl = Field(
        description="Internal service endpoint"
    )
    admin_endpoint: AnyHttpUrl = Field(
        description="Admin only service endpoint"
    )


class Service(OpenstackItem):
    enabled: bool = Field(description="Item is enabled")
    type: str = Field(description="Service type")
    endpoint: Optional[AnyHttpUrl] = Field(
        default=None, description="Public endpoint"
    )

    class Config:
        validate_assignment = True
