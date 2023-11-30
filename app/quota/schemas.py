"""Resource limitations for Projects on Services pydantic models."""
from typing import Literal, Optional

from pydantic import Field, validator

from app.models import BaseNode, BaseNodeCreate, BaseNodeRead
from app.query import create_query_model
from app.quota.enum import QuotaType


class QuotaBase(BaseNode):
    """Model with Quota basic attributes.

    Attributes:
    ----------
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
    """

    type: QuotaType = Field(description="Quota type.")
    per_user: bool = Field(default=False, description="Quota to apply for each user")


class BlockStorageQuotaBase(QuotaBase):
    """Model derived from ServiceBase to inherit attributes common to all services.

    It adds the basic attributes for BlockStorage services.

    Attributes:
    ----------
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        gigabytes (int | None): Number of max usable gigabytes (GiB).
        per_volume_gigabytes (int | None): Number of max usable gigabytes per volume
            (GiB).
        volumes (int | None): Number of max volumes a user group can create.
    """

    type: QuotaType = Field(
        default=QuotaType.BLOCK_STORAGE, description="Block storage type"
    )
    gigabytes: Optional[int] = Field(default=None, ge=-1, description="")
    per_volume_gigabytes: Optional[int] = Field(default=None, ge=-1, description="")
    volumes: Optional[int] = Field(default=None, ge=-1, description="")

    @validator("type", check_fields=False)
    def check_type(cls, v) -> Literal[QuotaType.BLOCK_STORAGE]:
        """Verify that type value is exactly QuotaType.BLOCK_STORAGE."""
        if v != QuotaType.BLOCK_STORAGE:
            raise ValueError(f"Not valid type: {v}")
        return v


class BlockStorageQuotaCreate(BaseNodeCreate, BlockStorageQuotaBase):
    """Model to create a Block Storage Quota.

    Class without id (which is populated by the database). Expected as input when
    performing a POST request.

    Attributes:
    ----------
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        gigabytes (int | None): Number of max usable gigabytes (GiB).
        per_volume_gigabytes (int | None): Number of max usable gigabytes per volume
            (GiB).
        volumes (int | None): Number of max volumes a user group can create.
    """


class BlockStorageQuotaUpdate(BaseNodeCreate, BlockStorageQuotaBase):
    """Model to update a Block Storage Quota.

    Class without id (which is populated by the database). Expected as input when
    performing a PUT request.

    Default to None attributes with a different default or required.

    Attributes:
    ----------
        description (str | None): Brief description.
        type (str | None): Quota type.
        per_user (str | None): This limitation should be applied to each user.
        gigabytes (int | None): Number of max usable gigabytes (GiB).
        per_volume_gigabytes (int | None): Number of max usable gigabytes per volume
            (GiB).
        volumes (int | None): Number of max volumes a user group can create.
    """


class BlockStorageQuotaRead(BaseNodeRead, BlockStorageQuotaBase):
    """Model to read Block Storage Quota data retrieved from DB.

    Class to read data retrieved from the database. Expected as output when performing a
    generic REST request. It contains all the non- sensible data written in the
    database.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        gigabytes (int | None): Number of max usable gigabytes (GiB).
        per_volume_gigabytes (int | None): Number of max usable gigabytes per volume
            (GiB).
        volumes (int | None): Number of max volumes a user group can create.
    """


class BlockStorageQuotaReadPublic(BaseNodeRead, BlockStorageQuotaBase):
    pass


class BlockStorageQuotaReadShort(BaseNodeRead, BlockStorageQuotaBase):
    pass


BlockStorageQuotaQuery = create_query_model(
    "BlockStorageQuotaQuery", BlockStorageQuotaBase
)


class ComputeQuotaBase(QuotaBase):
    """Model derived from ServiceBase to inherit attributes common to all services.

    It adds the basic attributes for Compute services.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        cores (int | None): Number of max usable cores.
        instance (int | None): Number of max VM instances.
        ram (int | None): Number of max usable RAM (MiB).
    """

    type: QuotaType = Field(default=QuotaType.COMPUTE, description="Compute type")
    cores: Optional[int] = Field(default=None, ge=0, description="")
    instances: Optional[int] = Field(default=None, ge=0, description="")
    ram: Optional[int] = Field(default=None, ge=0, description="")

    @validator("type", check_fields=False)
    def check_type(cls, v) -> Literal[QuotaType.COMPUTE]:
        """Verify that type value is exactly QuotaType.COMPUTE."""
        if v != QuotaType.COMPUTE:
            raise ValueError(f"Not valid type: {v}")
        return v


class ComputeQuotaCreate(BaseNodeCreate, ComputeQuotaBase):
    """Model to create a Compute Quota.

    Class without id (which is populated by the database). Expected as input when
    performing a POST request.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        cores (int | None): Number of max usable cores.
        instance (int | None): Number of max VM instances.
        ram (int | None): Number of max usable RAM (MiB).
    """


class ComputeQuotaUpdate(BaseNodeCreate, ComputeQuotaBase):
    """Model to update a Compute Quota.

    Class without id (which is populated by the database). Expected as input when
    performing a PUT request.

    Default to None attributes with a different default or required.

    Attributes:
    ----------
        uid (int | None): Quota unique ID.
        description (str | None): Brief description.
        type (str | None): Quota type.
        per_user (str | None): This limitation should be applied to each user.
        cores (int | None): Number of max usable cores.
        instance (int | None): Number of max VM instances.
        ram (int | None): Number of max usable RAM (MiB).
    """


class ComputeQuotaRead(BaseNodeRead, ComputeQuotaBase):
    """Model to read Compute Quota data retrieved from DB.

    Class to read data retrieved from the database. Expected as output when performing a
    generic REST request. It contains all the non- sensible data written in the
    database.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        cores (int | None): Number of max usable cores.
        instance (int | None): Number of max VM instances.
        ram (int | None): Number of max usable RAM (MiB).
    """


class ComputeQuotaReadPublic(BaseNodeRead, ComputeQuotaBase):
    pass


class ComputeQuotaReadShort(BaseNodeRead, ComputeQuotaBase):
    pass


ComputeQuotaQuery = create_query_model("ComputeQuotaQuery", ComputeQuotaBase)


class NetworkQuotaBase(QuotaBase):
    """Model derived from ServiceBase to inherit attributes common to all services.

    It adds the basic attributes for Network services.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        public_ips (int | None): The number of floating IP addresses allowed for each
            project.
        networks (int | None): The number of networks allowed for each project.
        port (int | None): The number of ports allowed for each project.
        security_groups (int | None): The number of security groups allowed for each
            project.
        security_group_rules (int | None): The number of security group rules allowed
            for each project.
    """

    type: QuotaType = Field(default=QuotaType.NETWORK, description="Network type")
    public_ips: Optional[int] = Field(
        default=None,
        ge=-1,
        description="The number of floating IP addresses allowed for each project.",
    )
    networks: Optional[int] = Field(
        default=None,
        ge=-1,
        description="The number of networks allowed for each project.",
    )
    ports: Optional[int] = Field(
        default=None, ge=-1, description="The number of ports allowed for each project."
    )
    security_groups: Optional[int] = Field(
        default=None,
        ge=-1,
        description="The number of security groups allowed for each project.",
    )
    security_group_rules: Optional[int] = Field(
        default=None,
        ge=-1,
        description="The number of security group rules allowed for each",
    )

    @validator("type", check_fields=False)
    def check_type(cls, v) -> Literal[QuotaType.NETWORK]:
        """Verify that type value is exactly QuotaType.NETWORK."""
        if v != QuotaType.NETWORK:
            raise ValueError(f"Not valid type: {v}")
        return v


class NetworkQuotaCreate(BaseNodeCreate, NetworkQuotaBase):
    """Model to create a Network Quota.

    Class without id (which is populated by the database). Expected as input when
    performing a POST request.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        public_ips (int | None): The number of floating IP addresses allowed for each
            project.
        networks (int | None): The number of networks allowed for each project.
        port (int | None): The number of ports allowed for each project.
        security_groups (int | None): The number of security groups allowed for each
            project.
        security_group_rules (int | None): The number of security group rules allowed
            for each project.
    """


class NetworkQuotaUpdate(BaseNodeCreate, NetworkQuotaBase):
    """Model to update a Network Quota.

    Class without id (which is populated by the database). Expected as input when
    performing a PUT request.

    Default to None attributes with a different default or required.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        public_ips (int | None): The number of floating IP addresses allowed for each
            project.
        networks (int | None): The number of networks allowed for each project.
        port (int | None): The number of ports allowed for each project.
        security_groups (int | None): The number of security groups allowed for each
            project.
        security_group_rules (int | None): The number of security group rules allowed
            for each project.
    """


class NetworkQuotaRead(BaseNodeRead, NetworkQuotaBase):
    """Model to read Network Quota data retrieved from DB.

    Class to read data retrieved from the database. Expected as output when performing a
    generic REST request. It contains all the non- sensible data written in the
    database.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        public_ips (int | None): The number of floating IP addresses allowed for each
            project.
        networks (int | None): The number of networks allowed for each project.
        port (int | None): The number of ports allowed for each project.
        security_groups (int | None): The number of security groups allowed for each
            project.
        security_group_rules (int | None): The number of security group rules allowed
            for each project.
    """


class NetworkQuotaReadPublic(BaseNodeRead, NetworkQuotaBase):
    pass


class NetworkQuotaReadShort(BaseNodeRead, NetworkQuotaBase):
    pass


NetworkQuotaQuery = create_query_model("NetworkQuotaQuery", NetworkQuotaBase)
