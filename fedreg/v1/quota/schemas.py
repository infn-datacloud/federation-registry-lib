"""Pydantic models of the Resource limitations for Projects on Services."""

from typing import Literal

from pydantic.v1 import Field

from fedreg.v1.core import (
    BaseNode,
    BaseNodeCreate,
    BaseNodeRead,
    BaseReadPrivate,
    BaseReadPublic,
    create_query_model,
)
from fedreg.v1.quota.constants import (
    DOC_BYTES,
    DOC_CONTAINERS,
    DOC_CORES,
    DOC_GB,
    DOC_GROUP_RULES,
    DOC_GROUPS,
    DOC_INST,
    DOC_NETS,
    DOC_OBJECTS,
    DOC_PER_USER,
    DOC_PORT,
    DOC_PUB_IPS,
    DOC_RAM,
    DOC_USAGE,
    DOC_VOL_GB,
    DOC_VOLS,
)
from fedreg.v1.quota.enum import QuotaType


class QuotaBase(BaseNode):
    """Model with Quota common attributes.

    This model is used also as a public interface.

    Attributes:
    ----------
        description (str): Brief description.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
    """

    per_user: bool = Field(default=False, description=DOC_PER_USER)
    usage: bool = Field(default=False, description=DOC_USAGE)


class BlockStorageQuotaBasePublic(QuotaBase):
    """Model with the Block Storage Quota public and restricted attributes.

    Model derived from QuotaBase to inherit attributes common to all quotas.

    Attributes:
    ----------
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        gigabytes (int | None): Number of max usable gigabytes (GiB).
        per_volume_gigabytes (int | None): Number of max usable gigabytes per volume
            (GiB).
        volumes (int | None): Number of max volumes a user group can create.
    """

    type: Literal[QuotaType.BLOCK_STORAGE] = Field(
        default=QuotaType.BLOCK_STORAGE, description="Block storage type"
    )


class BlockStorageQuotaBase(BlockStorageQuotaBasePublic):
    """Model with the Block Storage Quota public and restricted attributes.

    Model derived from QuotaBase to inherit attributes common to all quotas.

    Attributes:
    ----------
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        gigabytes (int | None): Number of max usable gigabytes (GiB).
        per_volume_gigabytes (int | None): Number of max usable gigabytes per volume
            (GiB).
        volumes (int | None): Number of max volumes a user group can create.
    """

    gigabytes: int | None = Field(default=None, ge=-1, description=DOC_GB)
    per_volume_gigabytes: int | None = Field(
        default=None, ge=-1, description=DOC_VOL_GB
    )
    volumes: int | None = Field(default=None, ge=-1, description=DOC_VOLS)
    pvcs: int | None = Field(
        default=None, ge=0, description="Total number of PVCs that can be created."
    )
    storage: int | None = Field(
        default=None,
        ge=0,
        description="Resources can define the minimum required storage. This is the "
        "maximum of the sum of all the resources' storage requests.",
    )
    requests_ephemeral_storage: int | None = Field(
        default=None,
        ge=0,
        description="Resources can define the minimum required ephemeral storage. This "
        "is the maximum of the sum of all the resources' ephemeral storage requests.",
    )
    limits_ephemeral_storage: int | None = Field(
        default=None,
        ge=0,
        description="Resources can define the maximum allowed ephemeral storage. This "
        "is the maximum of the sum of all the resources' ephemeral storage limits.",
    )


class BlockStorageQuotaCreate(BaseNodeCreate, BlockStorageQuotaBase):
    """Model to create a Block Storage Quota.

    Class without id (which is populated by the database). Expected as input when
    performing a POST request.

    Attributes:
    ----------
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
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
        usage (str): This quota defines the current resource usage.
        gigabytes (int | None): Number of max usable gigabytes (GiB).
        per_volume_gigabytes (int | None): Number of max usable gigabytes per volume
            (GiB).
        volumes (int | None): Number of max volumes a user group can create.
    """


class BlockStorageQuotaReadPublic(
    BaseNodeRead, BaseReadPublic, BlockStorageQuotaBasePublic
):
    """Model, for non-authenticated users, to read Block Storage data from DB.

    Class to read non-sensible data written in the DB. Expected as output when
    performing a generic REST request without authentication.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (str): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
    """


class BlockStorageQuotaRead(BaseNodeRead, BaseReadPrivate, BlockStorageQuotaBase):
    """Model, for authenticated users, to read Block Storage data from DB.

    Class to read all data written in the DB. Expected as output when performing a
    generic REST request with an authenticated user.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        gigabytes (int | None): Number of max usable gigabytes (GiB).
        per_volume_gigabytes (int | None): Number of max usable gigabytes per volume
            (GiB).
        volumes (int | None): Number of max volumes a user group can create.
    """


BlockStorageQuotaQuery = create_query_model(
    "BlockStorageQuotaQuery", BlockStorageQuotaBase
)


class StorageClassQuotaBasePublic(QuotaBase):
    """Model with the Block Storage Quota public and restricted attributes.

    Model derived from QuotaBase to inherit attributes common to all quotas.

    Attributes:
    ----------
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        gigabytes (int | None): Number of max usable gigabytes (GiB).
        per_volume_gigabytes (int | None): Number of max usable gigabytes per volume
            (GiB).
        volumes (int | None): Number of max volumes a user group can create.
    """

    type: Literal[QuotaType.STORAGECLASS] = Field(
        default=QuotaType.STORAGECLASS, description="Storageclass type"
    )


class StorageClassQuotaBase(StorageClassQuotaBasePublic):
    """Model with the Block Storage Quota public and restricted attributes.

    Model derived from QuotaBase to inherit attributes common to all quotas.

    Attributes:
    ----------
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        gigabytes (int | None): Number of max usable gigabytes (GiB).
        per_volume_gigabytes (int | None): Number of max usable gigabytes per volume
            (GiB).
        volumes (int | None): Number of max volumes a user group can create.
    """

    pvcs: int | None = Field(
        default=None,
        ge=0,
        description="Total number of PVCs that can be created for this kind of "
        "storageclass.",
    )
    storage: int | None = Field(
        default=None,
        ge=0,
        description="Resources can define the minimum required storage. This is the "
        "maximum of the sum of all the resources' storage requests.",
    )


class StorageClassQuotaCreate(BaseNodeCreate, StorageClassQuotaBase):
    """Model to create a Block Storage Quota.

    Class without id (which is populated by the database). Expected as input when
    performing a POST request.

    Attributes:
    ----------
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        gigabytes (int | None): Number of max usable gigabytes (GiB).
        per_volume_gigabytes (int | None): Number of max usable gigabytes per volume
            (GiB).
        volumes (int | None): Number of max volumes a user group can create.
    """


class StorageClassQuotaUpdate(BaseNodeCreate, StorageClassQuotaBase):
    """Model to update a Block Storage Quota.

    Class without id (which is populated by the database). Expected as input when
    performing a PUT request.

    Default to None attributes with a different default or required.

    Attributes:
    ----------
        description (str | None): Brief description.
        type (str | None): Quota type.
        per_user (str | None): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        gigabytes (int | None): Number of max usable gigabytes (GiB).
        per_volume_gigabytes (int | None): Number of max usable gigabytes per volume
            (GiB).
        volumes (int | None): Number of max volumes a user group can create.
    """


class StorageClassQuotaReadPublic(
    BaseNodeRead, BaseReadPublic, StorageClassQuotaBasePublic
):
    """Model, for non-authenticated users, to read Block Storage data from DB.

    Class to read non-sensible data written in the DB. Expected as output when
    performing a generic REST request without authentication.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (str): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
    """


class StorageClassQuotaRead(BaseNodeRead, BaseReadPrivate, StorageClassQuotaBase):
    """Model, for authenticated users, to read Block Storage data from DB.

    Class to read all data written in the DB. Expected as output when performing a
    generic REST request with an authenticated user.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        gigabytes (int | None): Number of max usable gigabytes (GiB).
        per_volume_gigabytes (int | None): Number of max usable gigabytes per volume
            (GiB).
        volumes (int | None): Number of max volumes a user group can create.
    """


StorageClassQuotaQuery = create_query_model(
    "StorageClassQuotaQuery", StorageClassQuotaBase
)


class ComputeQuotaBasePublic(QuotaBase):
    """Model with the Compute Quota public and restricted attributes.

    Model derived from QuotaBase to inherit attributes common to all quotas.

    Attributes:
    ----------
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        cores (int | None): Number of max usable cores.
        instances (int | None): Number of max VM instances.
        ram (int | None): Number of max usable RAM (MiB).
    """

    type: Literal[QuotaType.COMPUTE] = Field(
        default=QuotaType.COMPUTE, description="Compute type"
    )


class ComputeQuotaBase(ComputeQuotaBasePublic):
    """Model with the Compute Quota public and restricted attributes.

    Model derived from QuotaBase to inherit attributes common to all quotas.

    Attributes:
    ----------
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        cores (int | None): Number of max usable cores.
        instances (int | None): Number of max VM instances.
        ram (int | None): Number of max usable RAM (MiB).
        limits_cpu (int | None): Max value for the sum of the maximum usable cpus
            for a pod.
        requests_cpu (int | None): Max value for the sum of the "minimum required" cpus
            for a pod.
        limits_memory (int | None): Max value for the sum of the maximum usable memory
            for a pod.
        requests_memory (int | None): Max value for the sum of the "minimum required"
            memory for a pod.
        pods (int | None): Max number of pods that can be created.
        gpus (dict[str, int] | None): For each type of GPU, define the maximum quota.
    """

    cores: int | None = Field(default=None, ge=0, description=DOC_CORES)
    instances: int | None = Field(default=None, ge=0, description=DOC_INST)
    ram: int | None = Field(default=None, ge=0, description=DOC_RAM)
    limits_cpu: int | None = Field(
        default=None,
        ge=0,
        description="Max value for the sum of the maximum usable cpus for a pod.",
    )
    requests_cpu: int | None = Field(
        default=None,
        ge=0,
        description="Max value for the sum of the minimum required cpus for a pod.",
    )
    limits_memory: int | None = Field(
        default=None,
        ge=0,
        description="Max value for the sum of the maximum usable memory for a pod.",
    )
    requests_memory: int | None = Field(
        default=None,
        ge=0,
        description="Max value for the sum of the min required memory for a pod.",
    )
    pods: int | None = Field(
        default=None, ge=0, description="Max number of pods that can be created."
    )
    gpus: dict[str, int] | None = Field(
        default=None, description="For each type of GPU, define the maximum quota."
    )


class ComputeQuotaCreate(BaseNodeCreate, ComputeQuotaBase):
    """Model to create a Compute Quota.

    Class without id (which is populated by the database). Expected as input when
    performing a POST request.

    Attributes:
    ----------
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        cores (int | None): Number of max usable cores.
        instances (int | None): Number of max VM instances.
        ram (int | None): Number of max usable RAM (MiB).
    """


class ComputeQuotaUpdate(BaseNodeCreate, ComputeQuotaBase):
    """Model to update a Compute Quota.

    Class without id (which is populated by the database). Expected as input when
    performing a PUT request.

    Default to None attributes with a different default or required.

    Attributes:
    ----------
        description (str | None): Brief description.
        type (str | None): Quota type.
        per_user (str | None): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        cores (int | None): Number of max usable cores.
        instances (int | None): Number of max VM instances.
        ram (int | None): Number of max usable RAM (MiB).
    """


class ComputeQuotaReadPublic(BaseNodeRead, BaseReadPublic, ComputeQuotaBasePublic):
    """Model, for non-authenticated users, to read Compute data from DB.

    Class to read non-sensible data written in the DB. Expected as output when
    performing a generic REST request without authentication.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (str): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
    """


class ComputeQuotaRead(BaseNodeRead, BaseReadPrivate, ComputeQuotaBase):
    """Model, for authenticated users, to read Compute data from DB.

    Class to read all data written in the DB. Expected as output when performing a
    generic REST request with an authenticated user.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        cores (int | None): Number of max usable cores.
        instances (int | None): Number of max VM instances.
        ram (int | None): Number of max usable RAM (MiB).
    """


ComputeQuotaQuery = create_query_model("ComputeQuotaQuery", ComputeQuotaBase)


class NetworkQuotaBasePublic(QuotaBase):
    """Model with the Network Quota public and restricted attributes.

    Model derived from QuotaBase to inherit attributes common to all quotas.

    Attributes:
    ----------
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        public_ips (int | None): The number of floating IP addresses allowed for each
            project.
        networks (int | None): The number of networks allowed for each project.
        ports (int | None): The number of ports allowed for each project.
        security_groups (int | None): The number of security groups allowed for each
            project.
        security_group_rules (int | None): The number of security group rules allowed
            for each project.
    """

    type: Literal[QuotaType.NETWORK] = Field(
        default=QuotaType.NETWORK, description="Network type"
    )


class NetworkQuotaBase(NetworkQuotaBasePublic):
    """Model with the Network Quota public and restricted attributes.

    Model derived from QuotaBase to inherit attributes common to all quotas.

    Attributes:
    ----------
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        public_ips (int | None): The number of floating IP addresses allowed for each
            project.
        networks (int | None): The number of networks allowed for each project.
        ports (int | None): The number of ports allowed for each project.
        security_groups (int | None): The number of security groups allowed for each
            project.
        security_group_rules (int | None): The number of security group rules allowed
            for each project.
    """

    public_ips: int | None = Field(default=None, ge=-1, description=DOC_PUB_IPS)
    networks: int | None = Field(default=None, ge=-1, description=DOC_NETS)
    ports: int | None = Field(default=None, ge=-1, description=DOC_PORT)
    security_groups: int | None = Field(default=None, ge=-1, description=DOC_GROUPS)
    security_group_rules: int | None = Field(
        default=None, ge=-1, description=DOC_GROUP_RULES
    )


class NetworkQuotaCreate(BaseNodeCreate, NetworkQuotaBase):
    """Model to create a Network Quota.

    Class without id (which is populated by the database). Expected as input when
    performing a POST request.

    Attributes:
    ----------
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        public_ips (int | None): The number of floating IP addresses allowed for each
            project.
        networks (int | None): The number of networks allowed for each project.
        ports (int | None): The number of ports allowed for each project.
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
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        public_ips (int | None): The number of floating IP addresses allowed for each
            project.
        networks (int | None): The number of networks allowed for each project.
        ports (int | None): The number of ports allowed for each project.
        security_groups (int | None): The number of security groups allowed for each
            project.
        security_group_rules (int | None): The number of security group rules allowed
            for each project.
    """


class NetworkQuotaReadPublic(BaseNodeRead, BaseReadPublic, NetworkQuotaBasePublic):
    """Model, for non-authenticated users, to read Network data from DB.

    Class to read non-sensible data written in the DB. Expected as output when
    performing a generic REST request without authentication.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (str): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
    """

    type: QuotaType = Field(description="Network type")


class NetworkQuotaRead(BaseNodeRead, BaseReadPrivate, NetworkQuotaBase):
    """Model, for authenticated users, to read Network data from DB.

    Class to read all data written in the DB. Expected as output when performing a
    generic REST request with an authenticated user.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        public_ips (int | None): The number of floating IP addresses allowed for each
            project.
        networks (int | None): The number of networks allowed for each project.
        ports (int | None): The number of ports allowed for each project.
        security_groups (int | None): The number of security groups allowed for each
            project.
        security_group_rules (int | None): The number of security group rules allowed
            for each project.
    """


NetworkQuotaQuery = create_query_model("NetworkQuotaQuery", NetworkQuotaBase)


class ObjectStoreQuotaBasePublic(QuotaBase):
    """Model with the Object Storage Quota public and restricted attributes.

    Model derived from QuotaBase to inherit attributes common to all quotas.

    Attributes:
    ----------
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
    """

    type: Literal[QuotaType.OBJECT_STORE] = Field(
        default=QuotaType.OBJECT_STORE, description="Object storage type"
    )


class ObjectStoreQuotaBase(ObjectStoreQuotaBasePublic):
    """Model with the Object Storage Quota public and restricted attributes.

    Model derived from QuotaBase to inherit attributes common to all quotas.

    Attributes:
    ----------
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        bytes (int): Maximum number of allowed bytes.
        containers (int): Maximum number of allowed containers.
        objects (int): Maximum number of allowed objects.
    """

    bytes: int | None = Field(default=None, ge=-1, description=DOC_BYTES)
    containers: int | None = Field(default=None, ge=-1, description=DOC_CONTAINERS)
    objects: int | None = Field(default=None, ge=-1, description=DOC_OBJECTS)


class ObjectStoreQuotaCreate(BaseNodeCreate, ObjectStoreQuotaBase):
    """Model to create a Object Storage Quota.

    Class without id (which is populated by the database). Expected as input when
    performing a POST request.

    Attributes:
    ----------
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        bytes (int): Maximum number of allowed bytes.
        containers (int): Maximum number of allowed containers.
        objects (int): Maximum number of allowed objects
    """


class ObjectStoreQuotaUpdate(BaseNodeCreate, ObjectStoreQuotaBase):
    """Model to update a Object Storage Quota.

    Class without id (which is populated by the database). Expected as input when
    performing a PUT request.

    Default to None attributes with a different default or required.

    Attributes:
    ----------
        description (str | None): Brief description.
        type (str | None): Quota type.
        per_user (str | None): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        bytes (int): Maximum number of allowed bytes.
        containers (int): Maximum number of allowed containers.
        objects (int): Maximum number of allowed objects.
    """


class ObjectStoreQuotaReadPublic(
    BaseNodeRead, BaseReadPublic, ObjectStoreQuotaBasePublic
):
    """Model, for non-authenticated users, to read Object Storage data from DB.

    Class to read non-sensible data written in the DB. Expected as output when
    performing a generic REST request without authentication.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (str): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        bytes (int): Maximum number of allowed bytes.
        containers (int): Maximum number of allowed containers.
        objects (int): Maximum number of allowed objects
    """


class ObjectStoreQuotaRead(BaseNodeRead, BaseReadPrivate, ObjectStoreQuotaBase):
    """Model, for authenticated users, to read Object Storage data from DB.

    Class to read all data written in the DB. Expected as output when performing a
    generic REST request with an authenticated user.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        bytes (int): Maximum number of allowed bytes.
        containers (int): Maximum number of allowed containers.
        objects (int): Maximum number of allowed objects
    """


ObjectStoreQuotaQuery = create_query_model(
    "ObjectStoreQuotaQuery", ObjectStoreQuotaBase
)
