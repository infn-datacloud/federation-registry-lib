from typing import Union
from uuid import uuid4

from app.provider.schemas_extended import SLACreateExtended
from app.sla.models import SLA
from app.sla.schemas import (
    SLABase,
    SLARead,
    SLAReadPublic,
    SLAReadShort,
    SLAUpdate,
)
from app.sla.schemas_extended import SLAReadExtended, SLAReadExtendedPublic
from tests.utils.utils import random_date, random_lower_string


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
        **kwargs,
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


def validate_public_attrs(*, obj_in: SLABase, db_item: SLA) -> None:
    assert db_item.description == obj_in.description
    assert db_item.start_date == obj_in.start_date
    assert db_item.end_date == obj_in.end_date
    assert db_item.doc_uuid == obj_in.doc_uuid


def validate_attrs(*, obj_in: SLABase, db_item: SLA) -> None:
    validate_public_attrs(obj_in=obj_in, db_item=db_item)


def validate_rels(
    *, obj_out: Union[SLAReadExtended, SLAReadExtendedPublic], db_item: SLA
) -> None:
    db_user_group = db_item.user_group.single()
    assert db_user_group
    assert db_user_group.uid == obj_out.user_group.uid
    assert len(db_item.projects) == len(obj_out.projects)
    for db_proj, proj_out in zip(
        sorted(db_item.projects, key=lambda x: x.uid),
        sorted(obj_out.projects, key=lambda x: x.uid),
    ):
        assert db_proj.uid == proj_out.uid


def validate_create_sla_attrs(*, obj_in: SLACreateExtended, db_item: SLA) -> None:
    validate_attrs(obj_in=obj_in, db_item=db_item)
    assert obj_in.project in [i.uuid for i in db_item.projects]


def validate_read_sla_attrs(*, obj_out: SLARead, db_item: SLA) -> None:
    assert db_item.uid == obj_out.uid
    validate_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_short_sla_attrs(*, obj_out: SLAReadShort, db_item: SLA) -> None:
    assert db_item.uid == obj_out.uid
    validate_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_public_sla_attrs(*, obj_out: SLAReadPublic, db_item: SLA) -> None:
    assert db_item.uid == obj_out.uid
    validate_public_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_extended_sla_attrs(*, obj_out: SLAReadExtended, db_item: SLA) -> None:
    assert db_item.uid == obj_out.uid
    validate_attrs(obj_in=obj_out, db_item=db_item)
    validate_rels(obj_out=obj_out, db_item=db_item)


def validate_read_extended_public_sla_attrs(
    *, obj_out: SLAReadExtendedPublic, db_item: SLA
) -> None:
    assert db_item.uid == obj_out.uid
    validate_public_attrs(obj_in=obj_out, db_item=db_item)
    validate_rels(obj_out=obj_out, db_item=db_item)
