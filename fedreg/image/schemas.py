"""Pydantic models of the Virtual Machine Image owned by a Provider."""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

from fedreg.core import BaseNode, BaseNodeRead
from fedreg.image.enum import ImageOS


class ImageBase(BaseNode):
    """Model with Image public and restricted attributes.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Image name in the Provider.
        uuid (str): Image unique ID in the Provider
        os_type (str | None): OS type.
        os_distro (str | None): OS distribution.
        os_version (str | None): Distribution version.
        architecture (str | None): OS architecture.
        kernel_id (str | None): Kernel version.
        cuda_support (str): Support for cuda enabled.
        gpu_driver (str): Support for GPUs drivers enabled.
        created_at (datetime | None): Creation time.
        tags (list of str): list of tags associated to this Image.
    """

    name: Annotated[str, Field(description="Image name in the Resource Provider.")]
    uuid: Annotated[str, Field(description="Image unique ID in the Resource Provider.")]
    os_type: Annotated[ImageOS | None, Field(default=None, description="OS type.")]
    os_distro: Annotated[
        str | None, Field(default=None, description="OS distribution.")
    ]
    os_version: Annotated[
        str | None, Field(default=None, description="Distribution version.")
    ]
    architecture: Annotated[
        str | None, Field(default=None, description="OS architecture.")
    ]
    kernel_id: Annotated[str | None, Field(default=None, description="Kernel version.")]
    cuda_support: Annotated[
        bool, Field(default=False, description="Support for cuda enabled.")
    ]
    gpu_driver: Annotated[
        bool, Field(default=False, description="Support for GPUs drivers enabled.")
    ]
    created_at: Annotated[
        datetime | None, Field(default=None, description="Creation time")
    ]
    tags: Annotated[
        list[str],
        Field(
            default_factory=list, description="List of tags associated to this Image."
        ),
    ]


class ImageCreate(ImageBase):
    """Model to create an Image.

    Class without id (which is populated by the database). Expected as input when
    performing a POST request.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Image name in the Provider.
        uuid (str): Image unique ID in the Provider
        os_type (str | None): OS type.
        os_distro (str | None): OS distribution.
        os_version (str | None): Distribution version.
        architecture (str | None): OS architecture.
        kernel_id (str | None): Kernel version.
        cuda_support (str): Support for cuda enabled.
        gpu_driver (str): Support for GPUs drivers enabled.
        created_at (datetime | None): Creation time.
        tags (list of str): list of tags associated to this Image.
        is_shared (bool): Public or private Image.
    """


class ImageRead(BaseNodeRead, ImageBase):
    """Model, for authenticated users, to read Image data from DB.

    Class to read all data written in the DB. Expected as output when performing a
    generic REST request with an authenticated user.

    Add the *id* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        id (int): Image unique ID.
        description (str): Brief description.
        name (str): Image name in the Provider.
        uuid (str): Image unique ID in the Provider
        os_type (str | None): OS type.
        os_distro (str | None): OS distribution.
        os_version (str | None): Distribution version.
        architecture (str | None): OS architecture.
        kernel_id (str | None): Kernel version.
        cuda_support (str): Support for cuda enabled.
        gpu_driver (str): Support for GPUs drivers enabled.
        is_public (bool): Public or private Image.
        created_at (datetime | None): Creation time.
        tags (list of str): list of tags associated to this Image.
        is_shared (bool): Public or private Image.
    """


class ImageQuery(BaseModel):
    """Model to update an Image.

    Class without id (which is populated by the database). Expected as input when
    performing a PUT request.

    Default to None attributes with a different default or required.

    Attributes:
    ----------
        description (str | None): Brief description.
        name (str | None): Image name in the Provider.
        uuid (str | None): Image unique ID in the Provider
        os_type (str | None): OS type.
        os_distro (str | None): OS distribution.
        os_version (str | None): Distribution version.
        architecture (str | None): OS architecture.
        kernel_id (str | None): Kernel version.
        cuda_support (str | None): Support for cuda enabled.
        gpu_driver (str | None): Support for GPUs drivers enabled.
        created_at (datetime | None): Creation time.
        tags (list of str | None): list of tags associated to this Image.
    """

    name: Annotated[
        str | None,
        Field(default=None, description="Image name in the Resource Provider."),
    ]
    uuid: Annotated[
        str | None,
        Field(default=None, description="Image unique ID in the Resource Provider."),
    ]
    os_type: Annotated[str | None, Field(default=None, description="OS type.")]
    os_distro: Annotated[
        str | None, Field(default=None, description="OS distribution.")
    ]
    os_version: Annotated[
        str | None, Field(default=None, description="Distribution version.")
    ]
    architecture: Annotated[
        str | None, Field(default=None, description="OS architecture.")
    ]
    kernel_id: Annotated[str | None, Field(default=None, description="Kernel version.")]
    cuda_support: Annotated[
        bool | None, Field(default=None, description="Support for cuda enabled.")
    ]
    gpu_driver: Annotated[
        bool | None,
        Field(default=None, description="Support for GPUs drivers enabled."),
    ]
    created_at: Annotated[
        datetime | None, Field(default=None, description="Creation time")
    ]
    tags: Annotated[
        list[str] | None,
        Field(default=None, description="List of tags associated to this Image."),
    ]
