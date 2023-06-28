from pydantic import Field
from typing import List

from .schemas import SLA, SLACreate, SLAUpdate
from ..project.schemas import Project
from ..quota.schemas import QuotaUpdate
from ..quota.schemas_extended import QuotaCreateExtended, QuotaExtended
from ..user_group.schemas import UserGroup


class SLACreateExtended(SLACreate):
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

    quotas: List[QuotaCreateExtended]


class SLAUpdateExtended(SLAUpdate):
    """Service Level Agreement (SLA) Update Model class.

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

    quotas: List[QuotaUpdate] = Field(default_factory=list)


class SLAExtended(SLA):
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
    quotas: List[QuotaExtended]
