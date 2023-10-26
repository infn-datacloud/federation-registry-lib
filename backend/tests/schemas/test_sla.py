from datetime import timedelta
from uuid import uuid4

import pytest
from app.sla.models import SLA
from app.sla.schemas import SLARead, SLAReadPublic, SLAReadShort
from app.sla.schemas_extended import SLAReadExtended, SLAReadExtendedPublic
from pydantic import ValidationError
from tests.utils.sla import create_random_sla


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


def test_read_schema(db_sla: SLA):
    """Create a valid 'Read' Schema."""
    SLARead.from_orm(db_sla)
    SLAReadPublic.from_orm(db_sla)
    SLAReadShort.from_orm(db_sla)
    SLAReadExtended.from_orm(db_sla)
    SLAReadExtendedPublic.from_orm(db_sla)
