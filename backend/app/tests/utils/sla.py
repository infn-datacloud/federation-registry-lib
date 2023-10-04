from typing import List
from uuid import uuid4

from app.provider.schemas_extended import SLACreateExtended
from app.sla.models import SLA
from app.sla.schemas import SLAUpdate
from app.tests.utils.utils import random_date, random_datetime, random_lower_string
from pydantic import UUID4


def create_random_sla(
    *, default: bool = False, projects: List[UUID4] = []
) -> SLACreateExtended:
    doc_uuid = uuid4()
    d1 = random_date()
    d2 = random_date()
    if d1 < d2:
        start_date = d1
        end_date = d2
    else:
        start_date = d2
        end_date = d1
    kwargs = {}
    if not default:
        kwargs = {"description": random_lower_string()}
    if len(projects) > 0:
        kwargs["projects"] = projects
    return SLACreateExtended(
        start_date=start_date, end_date=end_date, doc_uuid=doc_uuid, **kwargs
    )


def create_random_update_sla_data() -> SLAUpdate:
    description = random_lower_string()
    start_date = random_datetime()
    end_date = random_datetime()
    return SLAUpdate(description=description, start_date=start_date, end_date=end_date)


def validate_sla_attrs(*, obj_in: SLACreateExtended, db_item: SLA) -> None:
    assert db_item.description == obj_in.description
    assert db_item.start_date == obj_in.start_date
    assert db_item.end_date == obj_in.end_date
    assert db_item.doc_uuid == str(obj_in.doc_uuid)
    assert len(db_item.projects) == len(obj_in.projects)
    for db_proj, proj_in in zip(db_item.projects, obj_in.projects):
        assert db_proj == proj_in
