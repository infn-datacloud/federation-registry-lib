from pydantic import Field
from typing import List

from ..nodes.cluster import Cluster
from ..nodes.flavor import Flavor
from ..nodes.image import Image
from ..nodes.user_group import UserGroup


class UserGroupExtended(UserGroup):
    """UserGroup class

    Class retrieved from the database
    expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        uid (uuid): UserGroup unique ID.
        name (str): UserGroup name.
        description (str): Brief description.
    """

    clusters: List[Cluster] = Field(default_factory=list)
    flavors: List[Flavor] = Field(default_factory=list)
    images: List[Image] = Field(default_factory=list)
