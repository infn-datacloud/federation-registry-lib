from datetime import datetime
from pydantic import UUID4, Field, validator
from typing import List, Optional

from ..models import BaseNodeCreate, BaseNodeQuery, BaseNodeRead
from ..project.schemas import Project
from ..quota.schemas import Quota, QuotaCreate
from ..user_group.schemas import UserGroup
from ..validators import get_all_nodes_from_rel, get_single_node_from_rel


class SLAQuery(BaseNodeQuery):
    """Service Level Agreement (SLA) Query Model class.

    Attributes:
        description (str | None): Brief description.
        start_date (datetime | None): SLA validity start date.
        end_date (datetime | None): SLA validity end date.
    """

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class SLAPatch(BaseNodeCreate):
    """Service Level Agreement (SLA) Patch Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH request.

    Attributes:
        description (str): Brief description.
        start_date (datetime | None): SLA validity start date.
        end_date (datetime | None): SLA validity end date.
        project (UUID4 | None): UUID4 of the target Project.
        user_group (UUID4 | None): UUID4 of the target UserGroup.
        quotas (list of QuotaCreate): List of quotas defined by the SLA.
    """

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    #project: Optional[UUID4] = None
    #user_group: Optional[UUID4] = None
    quotas: List[QuotaCreate] = Field(default_factory=list)


class SLACreate(SLAPatch):
    """Service Level Agreement (SLA) Create Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH, PUT or POST request.

    Attributes:
        description (str): Brief description.
        start_date (datetime): SLA validity start date.
        end_date (datetime): SLA validity end date.
        project (UUID4): UUID4 of the target Project.
        user_group (UUID4): UUID4 of the target UserGroup.
        quotas (list of QuotaCreate): List of quotas defined by the SLA.
    """

    start_date: datetime
    end_date: datetime
    project_uid: UUID4
    user_group_uid: UUID4
    quotas: List[QuotaCreate]


class SLA(SLACreate, BaseNodeRead):
    """Service Level Agreement (SLA) class.

    Class retrieved from the database.
    Expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        uid (uuid): Unique ID.
        description (str): Brief description.
        start_date (datetime): SLA validity start date.
        end_date (datetime): SLA validity end date.
        project (Project): UUID4 of the target Project.
        user_group (UserGroup): UUID4 of the target UserGroup.
        quotas (list of Quota): List of quotas defined by the SLA.
    """

    project: Project
    user_group: UserGroup
    quotas: List[Quota]

    _get_single_project = validator("project", pre=True, allow_reuse=True)(
        get_single_node_from_rel
    )
    _get_single_user_group = validator(
        "user_group", pre=True, allow_reuse=True
    )(get_single_node_from_rel)

    _get_all_quotas = validator("quotas", pre=True, allow_reuse=True)(
        get_all_nodes_from_rel
    )
