"""Core pydantic models."""

import math
from enum import Enum
from typing import Annotated, Any
from uuid import UUID

from neo4j.time import Date, DateTime
from neomodel import One, OneOrMore, ZeroOrMore, ZeroOrOne
from pydantic import (
    AnyHttpUrl,
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_validator,
)
from pydantic_core import PydanticUseDefault
from starlette.datastructures import URL


class BaseNode(BaseModel):
    """Common attributes and validators for a schema of a generic neo4j Node.

    Add description field and a validator converting UUIDs to str.

    Attributes:
    ----------
        description (str): Brief item description
    """

    description: Annotated[str, Field(default="", description="Brief item description")]

    @field_validator("*", mode="before")
    @classmethod
    def not_none(cls, v: Any) -> Any:
        """Before any check, return the default value if the field is None."""
        if v is None:
            raise PydanticUseDefault()
        return v

    @field_validator("*", mode="before")
    @classmethod
    def get_str_from_uuid(cls, v: Any) -> Any:
        """Get hex attribute from UUID values."""
        if isinstance(v, list):
            return [str(i) if isinstance(i, UUID) else i for i in v]
        return str(v) if isinstance(v, UUID) else v

    @field_validator("*", mode="after")
    @classmethod
    def get_value_from_enums(cls, v: Any) -> Any:
        """Get value from all the enumeration field values."""
        return v.value if isinstance(v, Enum) else v


class BaseNodeRead(BaseModel):
    """Common attributes and validators when reading nodes from the DB.

    Use ORM mode to read data from DB models.
    Add the id attribute.
    Convert Neo4j datetime objects into python
    datetime ones.
    When dealing with relationships retrieve all connected items and show
    them as an object list. If a relationships has a model return a dict with the data
    stored in it.
    Always validate assignments.

    Attributes:
    ----------
        id (str): Database item's unique identifier.
    """

    id: Annotated[
        str, Field(description="Database item's unique identifier.", alias="uid")
    ]

    @field_validator("*", mode="before")
    @classmethod
    def get_relationships(cls, v: Any) -> Any:
        """Cast neomodel relationships to lists.

        From One or ZeroOrOne relationships get that single relationship.
        From OneOrMore or ZeroOrMore relationships get all relationships.

        If the relationship has a model, return a dict with the data stored in the
        relationship.
        """
        if isinstance(v, (One, ZeroOrOne)):
            return v.single().id if v.single() is not None else None
        if isinstance(v, (OneOrMore, ZeroOrMore)):
            return [item.id for item in v.all()]
        return v

    @field_validator("*", mode="before")
    @classmethod
    def cast_neo4j_datetime_or_date(cls, v: Any) -> Any:
        """Cast neo4j datetime to python datetime or date."""
        return v.to_native() if isinstance(v, (Date, DateTime)) else v

    model_config = ConfigDict(from_attributes=True)


class PaginationQuery(BaseModel):
    """Model to filter lists in GET operations with multiple items."""

    size: Annotated[int, Field(default=5, ge=1, description="Chunk size.")]
    page: Annotated[
        int, Field(default=1, ge=1, description="Divide the list in chunks")
    ]
    sort: Annotated[
        str,
        Field(
            default="id",
            description="Name of the key to use to sort values. "
            "Prefix the '-' char to the chosen key to use reverse order.",
        ),
    ]


class Pagination(BaseModel):
    """With pagination details and total elements count."""

    size: Annotated[int, Field(default=5, ge=1, description="Chunk size.")]
    number: Annotated[
        int, Field(default=1, ge=1, description="Divide the list in chunks")
    ]
    total_elements: Annotated[int, Field(description="Total number of items")]

    @computed_field
    @property
    def total_pages(self) -> int:
        """Return the ceiling value of tot_items/page size.

        If there are no elements, there is still one page but with no items.
        """
        val = math.ceil(self.total_elements / self.size)
        return 1 if val == 0 else val


class PageNavigation(BaseModel):
    """Model with the navigation links to use to navigate through a paginated list."""

    first: Annotated[AnyHttpUrl, Field(description="Link to the first page")]
    prev: Annotated[
        AnyHttpUrl | None,
        Field(default=None, description="Link to the previous page if available"),
    ]
    next: Annotated[
        AnyHttpUrl | None,
        Field(default=None, description="Link to the next page if available"),
    ]
    last: Annotated[AnyHttpUrl, Field(description="Link to the last page")]


class PaginatedList(BaseModel):
    """Model with the pagination details and navigation links.

    Models with lists returned by GET operations MUST inherit from this model.
    """

    page_number: Annotated[int, Field(exclude=True, description="Current page number")]
    page_size: Annotated[int, Field(exclude=True, description="Current page size")]
    tot_items: Annotated[
        int,
        Field(
            exclude=True, description="Number of total items spread across al the pages"
        ),
    ]
    resource_url: Annotated[
        AnyHttpUrl,
        Field(
            exclude=True,
            description="Current resource URL. It may contain query parameters.",
        ),
    ]

    @computed_field
    @property
    def page(self) -> Pagination:
        """Return the pagination details."""
        return Pagination(
            number=self.page_number, size=self.page_size, total_elements=self.tot_items
        )

    @computed_field
    @property
    def links(self) -> PageNavigation:
        """Build navigation links for paginated API responses.

        Args:
            url: The base URL for navigation links.
            size: The number of items per page.
            curr_page: The current page number.
            tot_pages: The total number of pages available.

        Returns:
            PageNavigation: An object containing first, previous, next, and last page
                links.

        """
        url = URL(str(self.resource_url)).remove_query_params("page")
        first_page = url.include_query_params(page=1)._url
        if self.page_number > 1:
            prev_page = url.include_query_params(page=self.page_number - 1)._url
        else:
            prev_page = None

        if self.page_number < self.page.total_pages:
            next_page = url.include_query_params(page=self.page_number + 1)._url
        else:
            next_page = None
        last_page = url.include_query_params(page=self.page.total_pages)._url

        return PageNavigation(
            first=first_page, prev=prev_page, next=next_page, last=last_page
        )
