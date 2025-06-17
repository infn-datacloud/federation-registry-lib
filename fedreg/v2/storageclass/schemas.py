"""Pydantic models of the StorageClass owned by a Kubernetes Provider."""

from typing import Annotated

from pydantic import Field

from fedreg.v1.core import BaseNode, BaseNodeRead
from fedreg.v2.core import PaginationQuery


class StorageClassBase(BaseNode):
    """Represents the base schema for a StorageClass.

    Attributes:
        name (str): StorageClass name.
        provisioner (str): A provisioner determines what volume plugin is used for
            provisioning PVs
        is_default (bool): Indicates if this StorageClass is the cluster default one.
            Defaults to False.

    """

    name: Annotated[str, Field(description="StorageClass name")]
    provisioner: Annotated[
        str,
        Field(
            description="A provisioner determines what volume plugin is used for "
            "provisioning PVs"
        ),
    ]
    is_default: Annotated[
        bool,
        Field(default=False, description="StorageClass is the cluster default one"),
    ]


class StorageClassCreate(StorageClassBase):
    """
    Schema for creating a new StorageClass instance.

    Inherits from:
        StorageClassBase: Base schema with common StorageClass fields.

    Attributes:
        Inherits all attributes from StorageClassBase.

    """


class StorageClassRead(BaseNodeRead, StorageClassBase):
    """Represent a read-only schema for a storage class entity.

    Used for serializing and deserializing storage class data when reading from the
    database or API responses.

    Inherits from:
        BaseNodeRead: Provides base node read functionality.
        StorageClassBase: Contains base attributes for storage classes.

    Attributes:
        Inherits all attributes from BaseNodeRead and StorageClassBase.

    """


class StorageClassQuery(PaginationQuery):
    """Query parameters for filtering and paginating StorageClass resources.

    Attributes:
        name (str | None): StorageClass name to filter by. Optional.
        is_default (bool | None): Indicates if the StorageClass is the cluster default.
            Optional.

    """

    name: Annotated[str | None, Field(default=None, description="StorageClass name")]
    is_default: Annotated[
        bool | None,
        Field(default=None, description="StorageClass is the cluster default one"),
    ]
    provisioner: Annotated[
        str | None,
        Field(
            default=None,
            description="A provisioner determines what volume plugin is used for "
            "provisioning PVs",
        ),
    ]
