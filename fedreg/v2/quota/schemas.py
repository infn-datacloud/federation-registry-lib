"""Pydantic models of the  limitations for Projects on Services."""

from typing import Annotated, Literal

from pydantic import Field

from fedreg.v2.core import BaseNode, BaseNodeRead, PaginationQuery
from fedreg.v2.quota.enum import QuotaType


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


class OsBlockStorageQuotaCreate(QuotaBase):
    type: Annotated[
        Literal[QuotaType.BLOCK_STORAGE],
        Field(default=QuotaType.BLOCK_STORAGE, description="Block storage type"),
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
            description="Number of max volumes that can create.",
        ),
    ]


class K8sBlockStorageQuotaCreate(QuotaBase):
    type: Annotated[
        Literal[QuotaType.BLOCK_STORAGE],
        Field(default=QuotaType.BLOCK_STORAGE, description="Block storage type"),
    ]
    pvcs: Annotated[
        int | None,
        Field(
            default=None, ge=0, description="Total number of PVCs that can be created."
        ),
    ]
    storage: Annotated[
        int | None,
        Field(
            default=None,
            ge=0,
            description="Max value for the sum of the 'minimum required' gigabytes "
            "(GiB) for external storage.",
        ),
    ]
    requests_ephemeral_storage: Annotated[
        int | None,
        Field(
            default=None,
            ge=0,
            description="Resources can define the minimum required ephemeral storage. "
            "This is the maximum of the sum of all the resources' ephemeral storage "
            "requests.",
        ),
    ]
    limits_ephemeral_storage: Annotated[
        int | None,
        Field(
            default=None,
            ge=0,
            description="Resources can define the maximum allowed ephemeral storage. "
            "This is the maximum of the sum of all the resources' ephemeral storage "
            "limits.",
        ),
    ]


class K8sStorageClassQuotaCreate(QuotaBase):
    type: Annotated[
        Literal[QuotaType.STORAGECLASS],
        Field(default=QuotaType.STORAGECLASS, description="Block storage type"),
    ]
    pvcs: Annotated[
        int | None,
        Field(
            default=None,
            ge=0,
            description="Total number of PVCs that can be created for this kind of "
            "storageclass.",
        ),
    ]
    storage: Annotated[
        int | None,
        Field(
            default=None,
            ge=0,
            description="Max value for the sum of the 'minimum required' gigabytes "
            "(GiB) for this kind of storageclass.",
        ),
    ]


class OsComputeQuotaCreate(QuotaBase):
    type: Annotated[
        Literal[QuotaType.COMPUTE],
        Field(default=QuotaType.COMPUTE, description="Compute type"),
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


class K8sComputeQuotaCreate(QuotaBase):
    type: Annotated[
        Literal[QuotaType.COMPUTE],
        Field(default=QuotaType.COMPUTE, description="Compute type"),
    ]
    limits_cpu: Annotated[
        int | None,
        Field(
            default=None,
            ge=0,
            description="Max value for the sum of the maximum usable cpus for a pod.",
        ),
    ]
    requests_cpu: Annotated[
        int | None,
        Field(
            default=None,
            ge=0,
            description="Max value for the sum of the minimum required cpus for a pod.",
        ),
    ]
    limits_memory: Annotated[
        int | None,
        Field(
            default=None,
            ge=0,
            description="Max value for the sum of the maximum usable memory for a pod.",
        ),
    ]
    requests_memory: Annotated[
        int | None,
        Field(
            default=None,
            ge=0,
            description="Max value for the sum of the min required memory for a pod.",
        ),
    ]
    pods: Annotated[
        int | None,
        Field(
            default=None, ge=0, description="Max number of pods that can be created."
        ),
    ]
    gpus: Annotated[
        dict[str, int] | None,
        Field(
            default=None, description="For each type of GPU, define the maximum quota."
        ),
    ]


class OsNetworkQuotaCreate(QuotaBase):
    type: Annotated[
        Literal[QuotaType.NETWORKING],
        Field(default=QuotaType.NETWORKING, description="Network type"),
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
        Literal[QuotaType.OBJECT_STORE],
        Field(default=QuotaType.OBJECT_STORE, description="Object storage type"),
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
    type: Annotated[QuotaType, Field(description="Quota type")]
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
    pvcs: Annotated[
        int | None,
        Field(
            default=None, ge=0, description="Total number of PVCs that can be created."
        ),
    ]
    storage: Annotated[
        int | None,
        Field(
            default=None,
            ge=0,
            description="Max value for the sum of the 'minimum required' gigabytes "
            "(GiB) for external storage.",
        ),
    ]
    requests_ephemeral_storage: Annotated[
        int | None,
        Field(
            default=None,
            ge=0,
            description="Resources can define the minimum required ephemeral storage. "
            "This is the maximum of the sum of all the resources' ephemeral storage "
            "requests.",
        ),
    ]
    limits_ephemeral_storage: Annotated[
        int | None,
        Field(
            default=None,
            ge=0,
            description="Resources can define the maximum allowed ephemeral storage. "
            "This is the maximum of the sum of all the resources' ephemeral storage "
            "limits.",
        ),
    ]
    storageclass: Annotated[
        str | None,
        Field(
            default=None,
            description="When the quota points to a specific storageclass, this field "
            "points to the unique ID of the storage class",
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
    pvcs: Annotated[
        int | None,
        Field(
            default=None, ge=0, description="Total number of PVCs that can be created."
        ),
    ]
    storage: Annotated[
        int | None,
        Field(
            default=None,
            ge=0,
            description="Max value for the sum of the 'minimum required' gigabytes "
            "(GiB) for external storage.",
        ),
    ]
    requests_ephemeral_storage: Annotated[
        int | None,
        Field(
            default=None,
            ge=0,
            description="Resources can define the minimum required ephemeral storage. "
            "This is the maximum of the sum of all the resources' ephemeral storage "
            "requests.",
        ),
    ]
    limits_ephemeral_storage: Annotated[
        int | None,
        Field(
            default=None,
            ge=0,
            description="Resources can define the maximum allowed ephemeral storage. "
            "This is the maximum of the sum of all the resources' ephemeral storage "
            "limits.",
        ),
    ]
