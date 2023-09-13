from typing import Optional

from app.models import BaseNodeCreate, BaseNodeRead
from app.query import create_query_model
from app.service.enum import ServiceName
from pydantic import BaseModel, Extra, Field, validator


class QuotaBase(BaseModel, extra=Extra.allow):
    """Model with Quota basic attributes."""

    type: ServiceName = Field(description="Service type.")


class QuotaCreate(BaseNodeCreate, QuotaBase):
    """Model to create a Quota.

    Class without id (which is populated by the database). Expected as
    input when performing a POST request.
    """


class QuotaUpdate(QuotaCreate):
    """Model to update a Quota.

    Class without id (which is populated by the database). Expected as
    input when performing a PUT request.

    Default to None mandatory attributes.
    """


class QuotaRead(BaseNodeRead, QuotaBase):
    """Model to read Service data retrieved from DB.

    Class to read data retrieved from the database. Expected as output
    when performing a generic REST request. It contains all the non-
    sensible data written in the database.

    Add the *uid* attribute, which is the item unique identifier in the
    database.
    """


class QuotaReadPublic(BaseNodeRead, QuotaBase):
    pass


class QuotaReadShort(BaseNodeRead, QuotaBase):
    pass


QuotaQuery = create_query_model("QuotaQuery", QuotaBase)


class NovaBase(QuotaBase, extra=Extra.ignore):
    """Model derived from ServiceBase to inherit attributes common to all
    services. It adds the basic attributes for Nova services.

    Validation: type value is exactly ServiceType.openstack_nova.
    """

    cores: Optional[int] = Field(default=None, description="")
    fixed_ips: Optional[int] = Field(default=None, description="")
    floating_ips: Optional[int] = Field(default=None, description="")
    force: Optional[bool] = Field(default=None, description="")
    injected_file_content_bytes: Optional[int] = Field(default=None, description="")
    injected_file_path_bytes: Optional[int] = Field(default=None, description="")
    injected_files: Optional[int] = Field(default=None, description="")
    instances: Optional[int] = Field(default=None, description="")
    key_pairs: Optional[int] = Field(default=None, description="")
    metadata_items: Optional[int] = Field(default=None, description="")
    networks: Optional[int] = Field(default=None, description="")
    ram: Optional[int] = Field(default=None, description="")
    security_group_rules: Optional[int] = Field(default=None, description="")
    security_groups: Optional[int] = Field(default=None, description="")
    server_groups: Optional[int] = Field(default=None, description="")
    server_group_members: Optional[int] = Field(default=None, description="")

    @validator("type", check_fields=False)
    def check_type(cls, v):
        if v != ServiceName.OPENSTACK_NOVA:
            raise ValueError(f"Not valid type: {v}")
        return v


class NovaQuotaCreate(BaseNodeCreate, NovaBase):
    pass


class NovaQuotaUpdate(NovaQuotaCreate):
    pass


class NovaQuotaRead(BaseNodeRead, NovaBase):
    pass


class NovaQuotaReadPublic(BaseNodeRead, NovaBase):
    pass


class NovaQuotaReadShort(BaseNodeRead, NovaBase):
    pass


NovaQuotaQuery = create_query_model("NovaQuotaQuery", NovaBase)
