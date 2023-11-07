from datetime import timedelta
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.sla.models import SLA
from app.sla.schemas import SLARead, SLAReadPublic, SLAReadShort
from app.sla.schemas_extended import SLAReadExtended, SLAReadExtendedPublic
from tests.utils.sla import (
    create_random_sla,
    validate_read_extended_public_sla_attrs,
    validate_read_extended_sla_attrs,
    validate_read_public_sla_attrs,
    validate_read_short_sla_attrs,
    validate_read_sla_attrs,
)


def test_create_schema():
    """Create a valid 'Create' Schema."""
    create_random_sla(project=uuid4())
    create_random_sla(default=True, project=uuid4())


def test_invalid_create_schema():
    """List all invalid situations for a 'Create' Schema."""
    a = create_random_sla(project=uuid4())
    with pytest.raises(ValidationError):
        a.doc_uuid = None
    with pytest.raises(ValidationError):
        a.project = None
    with pytest.raises(ValidationError):
        # End date must be greater then start date
        a.start_date = a.end_date
    with pytest.raises(ValidationError):
        # End date must be greater then start date
        a.end_date = a.start_date - timedelta(1)


def test_read_schema_with_one_project(db_sla: SLA):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them should raise
    errors.

    Target SLA has one project.
    """
    schema = SLARead.from_orm(db_sla)
    validate_read_sla_attrs(obj_out=schema, db_item=db_sla)
    schema = SLAReadShort.from_orm(db_sla)
    validate_read_short_sla_attrs(obj_out=schema, db_item=db_sla)
    schema = SLAReadPublic.from_orm(db_sla)
    validate_read_public_sla_attrs(obj_out=schema, db_item=db_sla)
    schema = SLAReadExtended.from_orm(db_sla)
    validate_read_extended_sla_attrs(obj_out=schema, db_item=db_sla)
    schema = SLAReadExtendedPublic.from_orm(db_sla)
    validate_read_extended_public_sla_attrs(obj_out=schema, db_item=db_sla)


# TODO
# def test_read_schema_with_multiple_projects(db_sla_with_multiple_projects: SLA):
#     """Create a valid 'Read' Schema from DB object.

#     Apply conversion for this item for all read
#     schemas. No one of them should raise errors.

#     Target SLA has multiple projects."""
#     schema = SLARead.from_orm(db_sla_with_multiple_projects)
#     validate_read_sla_attrs(obj_out=schema, db_item=db_sla_with_multiple_projects)
#     schema = SLAReadShort.from_orm(db_sla_with_multiple_projects)
#     validate_read_short_sla_attrs(obj_out=schema,
#         db_item=db_sla_with_multiple_projects)
#     schema = SLAReadPublic.from_orm(db_sla_with_multiple_projects)
#     validate_read_public_sla_attrs(
#         obj_out=schema, db_item=db_sla_with_multiple_projects
#     )
#     schema = SLAReadExtended.from_orm(db_sla_with_multiple_projects)
#     validate_read_extended_sla_attrs(
#         obj_out=schema, db_item=db_sla_with_multiple_projects
#     )
#     schema = SLAReadExtendedPublic.from_orm(db_sla_with_multiple_projects)
#     validate_read_extended_public_sla_attrs(
#         obj_out=schema, db_item=db_sla_with_multiple_projects
#     )
