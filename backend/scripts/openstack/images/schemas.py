from datetime import datetime
from typing import Optional

from pydantic import Field
from scripts.openstack.images.enum import (
    ContainerFormat,
    DiskFormat,
    Status,
    Visibility,
)
from scripts.openstack.schemas import OpenstackItem


class Image(OpenstackItem):
    container_format: Optional[ContainerFormat] = Field(
        description="Format of the image container."
    )
    created_at: datetime = Field(
        description="The date and time when the resource was created."
    )
    disk_format: Optional[DiskFormat] = Field(
        description="The format of the disk."
    )
    min_disk: Optional[int] = Field(
        description="Amount of disk space in GB that is required to boot the image."
    )
    min_ram: Optional[int] = Field(
        description="Amount of RAM in MB that is required to boot the image"
    )
    name: Optional[str] = Field(description="Item name")
    owner: Optional[str] = Field(
        description="An identifier for the owner of the image, \
            usually the project uuid."
    )
    status: Status = Field(description="The image status.")
    updated_at: Optional[datetime] = Field(
        description="The date and time when the resource was updated."
    )
    visibility: Visibility = Field(
        description="Image visibility, that is, the access permission for the image."
    )
