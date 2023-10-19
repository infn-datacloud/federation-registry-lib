from datetime import timedelta
from uuid import uuid4

import pytest
from app.sla.crud import sla
from app.sla.schemas import SLARead, SLAReadPublic, SLAReadShort
from app.sla.schemas_extended import SLAReadExtended, SLAReadExtendedPublic
from app.tests.utils.sla import create_random_sla
from app.user_group.models import UserGroup
from pydantic import ValidationError


def test_create_schema():
    """Create a valid 'Create' Schema."""
    create_random_sla(projects=[uuid4()])
    create_random_sla(default=True, projects=[uuid4()])


def test_invalid_create_schema():
    """List all invalid situations for a 'Create' Schema."""
    a = create_random_sla(projects=[uuid4()])
    with pytest.raises(ValidationError):
        a.doc_uuid = None
    with pytest.raises(ValidationError):
        # End date must be greater then start date
        a.start_date = a.end_date
    with pytest.raises(ValidationError):
        # End date must be greater then start date
        a.end_date = a.start_date - timedelta(1)
    with pytest.raises(ValidationError):
        # Duplicated projects
        a.projects = [a.projects[0], a.projects[0]]


def test_read_schema(db_group: UserGroup):
    """Create a valid 'Read' Schema."""
    db_identity_provider = db_group.identity_provider.single()
    db_provider = db_identity_provider.providers.all()[0]

    obj_in = create_random_sla(projects=[i.uuid for i in db_provider.projects])
    db_obj = sla.create(
        obj_in=obj_in, user_group=db_group, projects=db_provider.projects
    )
    SLARead.from_orm(db_obj)
    SLAReadPublic.from_orm(db_obj)
    SLAReadShort.from_orm(db_obj)
    SLAReadExtended.from_orm(db_obj)
    SLAReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_sla(
        default=True, projects=[i.uuid for i in db_provider.projects]
    )
    db_obj = sla.update(
        db_obj=db_obj, obj_in=obj_in, projects=db_provider.projects, force=True
    )
    SLARead.from_orm(db_obj)
    SLAReadPublic.from_orm(db_obj)
    SLAReadShort.from_orm(db_obj)
    SLAReadExtended.from_orm(db_obj)
    SLAReadExtendedPublic.from_orm(db_obj)
