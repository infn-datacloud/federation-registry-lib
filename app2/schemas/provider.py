from pydantic import BaseModel, Field
from typing import List
from uuid import UUID

from .sla import SLA


class ProviderBase(BaseModel):
    """Provider Base class

    Class without id which is populated by the database.

    Attributes:
        name (str): Provider name.
        is_public (bool): Public Provider.
        slas (list of SLA): List of SLAs related to the Provider.
        # TODO: Country name, code and location can be grouped in
        a separate entity.
    """

    name: str
    description: str = ""
    is_public: bool = False
    support_email: List[str] = Field(default_factory=list)
    #slas: List[SLA] = Field(default_factory=list)

    class Config:
        validate_assignment = True


class ProviderCreate(ProviderBase):
    """Provider Create class

    Class expected as input when performing a REST request.

    Attributes:
        name (str): Provider name.
        is_public (bool): Public Provider.
        slas (list of SLA): List of SLAs related to the Provider.
        # TODO: Country name, code and location can be grouped in
        a separate entity.
    """

    pass


class Provider(ProviderBase):
    """Provider class

    Class expected as output when performing a REST request.
    It contains all the non-sensible data written in the database.

    Attributes:
        id (int): Provider unique ID.
        name (str): Provider name.
        is_public (bool): Public Provider.
        slas (list of SLA): List of SLAs related to the Provider.
        # TODO: Country name, code and location can be grouped in
        a separate entity.
    """

    id: UUID

    class Config:
        orm_mode = True
