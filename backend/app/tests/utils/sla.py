from uuid import uuid4

from app.provider.schemas_extended import SLACreateExtended
from app.sla.models import SLA
from app.sla.schemas import SLAUpdate
from app.tests.utils.utils import random_date, random_lower_string


def create_random_sla(*, default: bool = False, project: str) -> SLACreateExtended:
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
    return SLACreateExtended(
        start_date=start_date,
        end_date=end_date,
        doc_uuid=doc_uuid,
        project=project,
        **kwargs
    )


def create_random_sla_patch(*, default: bool = False) -> SLAUpdate:
    if default:
        return SLAUpdate()
    description = random_lower_string()
    doc_uuid = uuid4()
    d1 = random_date()
    d2 = random_date()
    if d1 < d2:
        start_date = d1
        end_date = d2
    else:
        start_date = d2
        end_date = d1
    return SLAUpdate(
        doc_uuid=doc_uuid,
        description=description,
        start_date=start_date,
        end_date=end_date,
    )


def validate_sla_attrs(*, obj_in: SLACreateExtended, db_item: SLA) -> None:
    assert db_item.description == obj_in.description
    assert db_item.start_date == obj_in.start_date
    assert db_item.end_date == obj_in.end_date
    assert db_item.doc_uuid == obj_in.doc_uuid
    assert obj_in.project in [i.uuid for i in db_item.projects]
