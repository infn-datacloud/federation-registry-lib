from typing import List
from uuid import UUID
from pydantic import BaseModel, Field

from .flavor import Flavor
from .image import Image
from .sla import SLA


class ProjectBase(BaseModel):
    """Project Base class.

    Class without id which is populated by the database.

    Attributes:
        name (str): Project name.
        images (list of Image): List of the images belonged by the Project.
        flavors (list of Flavor): List of the flavors belonged by the Project.
    """

    name: str
    #images: List[Image] = Field(default_factory=list)
    #flavors: List[Flavor] = Field(default_factory=list)
    #slas: List[SLA] = Field(default_factory=list)

    class Config:
        validate_assignment = True


class ProjectCreate(ProjectBase):
    """Project Create class.

    Class expected as input when performing a REST request.

    Attributes:
        name (str): Project name.
        images (list of Image): List of the images belonged by the Project.
        flavors (list of Flavor): List of the flavors belonged by the Project.
    """

    pass


class Project(ProjectBase):
    """Project class

    Class expected as output when performing a REST request.
    It contains all the non-sensible data written in the database.

    Attributes:
        id (str): Project unique ID.
        name (str): Project name.
        images (list of Image): List of the images belonged by the Project.
        flavors (list of Flavor): List of the flavors belonged by the Project.
    """

    id: UUID

    class Config:
        orm_mode = True
