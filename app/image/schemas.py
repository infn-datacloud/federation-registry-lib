"""Pydantic models of the Virtual Machine Image owned by a Provider."""
from typing import List, Optional

from pydantic import Field

from app.image.enum import ImageOS
from app.models import BaseNode, BaseNodeCreate, BaseNodeRead
from app.query import create_query_model


class ImageBasePublic(BaseNode):
    """Model with Image public attributes.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Image name in the Provider.
        uuid (str): Image unique ID in the Provider
    """

    name: str = Field(description="Image name in the provider.")
    uuid: str = Field(description="Image UUID in the provider.")


class ImageBase(ImageBasePublic):
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
        gpu_driver (str): Support for GPUs drivers.
        is_public (bool): Public or private Image.
        tags (list of str): List of tags associated to this Image.
    """

    os_type: Optional[ImageOS] = Field(
        default=None, description="Image Operating System."
    )
    os_distro: Optional[str] = Field(
        default=None, description="Operating system distribution type."
    )
    os_version: Optional[str] = Field(default=None, description="Distribution version.")
    architecture: Optional[str] = Field(
        default=None, description="Operating system architecture."
    )
    kernel_id: Optional[str] = Field(default=None, description="Kernel version")
    cuda_support: bool = Field(default=False, description="Enable CUDA support.")
    gpu_driver: bool = Field(default=False, description="Enable GPU driver support.")
    is_public: bool = Field(default=True, description="Public available")
    tags: List[str] = Field(default_factory=list, description="List of tags")


class ImageCreate(BaseNodeCreate, ImageBase):
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
        gpu_driver (str): Support for GPUs drivers.
        is_public (bool): Public or private Image.
        tags (list of str): List of tags associated to this Image.
    """


class ImageUpdate(BaseNodeCreate, ImageBase):
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
        gpu_driver (str | None): Support for GPUs drivers.
        is_public (bool | None): Public or private Image.
        tags (list of str | None): List of tags associated to this Image.
    """

    name: Optional[str] = Field(default=None, description="Image name in the provider.")
    uuid: Optional[str] = Field(default=None, description="Image UUID in the provider.")


class ImageReadPublic(BaseNodeRead, ImageBasePublic):
    """Model, for non-authenticated users, to read Image data from DB.

    Class to read non-sensible data written in the DB. Expected as output when
    performing a generic REST request without authentication.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (str): Image unique ID.
        description (str): Brief description.
        name (str): Image name in the Provider.
        uuid (str): Image unique ID in the Provider
    """


class ImageRead(BaseNodeRead, ImageBase):
    """Model, for authenticated users, to read Image data from DB.

    Class to read all data written in the DB. Expected as output when performing a
    generic REST request with an authenticated user.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (int): Image unique ID.
        description (str): Brief description.
        name (str): Image name in the Provider.
        uuid (str): Image unique ID in the Provider
        os_type (str | None): OS type.
        os_distro (str | None): OS distribution.
        os_version (str | None): Distribution version.
        architecture (str | None): OS architecture.
        kernel_id (str | None): Kernel version.
        cuda_support (str): Support for cuda enabled.
        gpu_driver (str): Support for GPUs drivers.
        is_public (bool): Public or private Image.
        tags (list of str): List of tags associated to this Image.
    """


ImageQuery = create_query_model("ImageQuery", ImageBase)
