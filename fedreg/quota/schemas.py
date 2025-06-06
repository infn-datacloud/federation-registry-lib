"""Pydantic models of the  limitations for Projects on Services."""

from typing import Annotated, Literal

from pydantic import Field

from fedreg.core import BaseNode, BaseNodeRead, PaginationQuery
from fedreg.service.enum import ServiceType


class QuotaBase(BaseNode):
    per_user: Annotated[
        bool,
        Field(
            default=False,
            description="This limitation or usage should be applied to each user.",
        ),
    ]
    usage: Annotated[
        bool,
        Field(
            default=False,
            description="Flag to determine if this quota represents the current usage "
            "(true) or the maximum resources (false).",
        ),
    ]
    service: Annotated[str, Field(description="Target service ID. Same type of quota.")]


class BlockStorageQuotaCreate(QuotaBase):
    type: Annotated[
        Literal[ServiceType.BLOCK_STORAGE],
        Field(default=ServiceType.BLOCK_STORAGE, description="Block storage type"),
    ]
    gigabytes: Annotated[
        int | None,
        Field(default=None, ge=-1, description="Number of max usable gigabytes (GiB)."),
    ]
    per_volume_gigabytes: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="Number of max usable gigabytes per volume (GiB).",
        ),
    ]
    volumes: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="Number of max volumes a user group can create.",
        ),
    ]


class ComputeQuotaCreate(QuotaBase):
    type: Annotated[
        Literal[ServiceType.COMPUTE],
        Field(default=ServiceType.COMPUTE, description="Compute type"),
    ]
    cores: Annotated[
        int | None, Field(default=None, ge=0, description="Number of max usable cores.")
    ]
    instances: Annotated[
        int | None, Field(default=None, ge=0, description="Number of max VM instances.")
    ]
    ram: Annotated[
        int | None,
        Field(default=None, ge=0, description="Number of max usable RAM (MiB)."),
    ]


class NetworkQuotaCreate(QuotaBase):
    type: Annotated[
        Literal[ServiceType.NETWORKING],
        Field(default=ServiceType.NETWORKING, description="Network type"),
    ]
    public_ips: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="The number of floating IP addresses allowed for each project.",
        ),
    ]
    networks: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="The number of networks allowed for each project.",
        ),
    ]
    ports: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="The number of ports allowed for each project.",
        ),
    ]
    security_groups: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="The number of security groups allowed for each project.",
        ),
    ]
    security_group_rules: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="The number of security group rules allowed for each project.",
        ),
    ]


class ObjectStoreQuotaCreate(QuotaBase):
    type: Annotated[
        Literal[ServiceType.OBJECT_STORE],
        Field(default=ServiceType.OBJECT_STORE, description="Object storage type"),
    ]
    bytes: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="Number of max usable bytes on all containers (B).",
        ),
    ]
    containers: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="The number of containers allowed for each project.",
        ),
    ]
    objects: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="The number of objects allowed for each project.",
        ),
    ]


class QuotaRead(BaseNodeRead, QuotaBase):
    type: Annotated[ServiceType, Field(description="Block storage type")]
    gigabytes: Annotated[
        int | None,
        Field(default=None, ge=-1, description="Number of max usable gigabytes (GiB)."),
    ]
    per_volume_gigabytes: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="Number of max usable gigabytes per volume (GiB).",
        ),
    ]
    volumes: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="Number of max volumes a user group can create.",
        ),
    ]
    cores: Annotated[
        int | None, Field(default=None, ge=0, description="Number of max usable cores.")
    ]
    instances: Annotated[
        int | None, Field(default=None, ge=0, description="Number of max VM instances.")
    ]
    ram: Annotated[
        int | None,
        Field(default=None, ge=0, description="Number of max usable RAM (MiB)."),
    ]
    public_ips: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="The number of floating IP addresses allowed for each project.",
        ),
    ]
    networks: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="The number of networks allowed for each project.",
        ),
    ]
    ports: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="The number of ports allowed for each project.",
        ),
    ]
    security_groups: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="The number of security groups allowed for each project.",
        ),
    ]
    security_group_rules: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="The number of security group rules allowed for each project.",
        ),
    ]
    bytes: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="Number of max usable bytes on all containers (B).",
        ),
    ]
    containers: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="The number of containers allowed for each project.",
        ),
    ]
    objects: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="The number of objects allowed for each project.",
        ),
    ]


class QuotaQuery(PaginationQuery):
    type: Annotated[str | None, Field(default=None, description="Block storage type")]
    gigabytes: Annotated[
        int | None,
        Field(default=None, ge=-1, description="Number of max usable gigabytes (GiB)."),
    ]
    per_volume_gigabytes: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="Number of max usable gigabytes per volume (GiB).",
        ),
    ]
    volumes: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="Number of max volumes a user group can create.",
        ),
    ]
    cores: Annotated[
        int | None, Field(default=None, ge=0, description="Number of max usable cores.")
    ]
    instances: Annotated[
        int | None, Field(default=None, ge=0, description="Number of max VM instances.")
    ]
    ram: Annotated[
        int | None,
        Field(default=None, ge=0, description="Number of max usable RAM (MiB)."),
    ]
    public_ips: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="The number of floating IP addresses allowed for each project.",
        ),
    ]
    networks: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="The number of networks allowed for each project.",
        ),
    ]
    ports: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="The number of ports allowed for each project.",
        ),
    ]
    security_groups: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="The number of security groups allowed for each project.",
        ),
    ]
    security_group_rules: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="The number of security group rules allowed for each project.",
        ),
    ]
    bytes: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="Number of max usable bytes on all containers (B).",
        ),
    ]
    containers: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="The number of containers allowed for each project.",
        ),
    ]
    objects: Annotated[
        int | None,
        Field(
            default=None,
            ge=-1,
            description="The number of objects allowed for each project.",
        ),
    ]
