from uuid import uuid4

import pytest
from app.quota.crud import compute_quota
from app.quota.enum import QuotaType
from app.quota.schemas import (
    ComputeQuotaRead,
    ComputeQuotaReadPublic,
    ComputeQuotaReadShort,
)
from app.quota.schemas_extended import (
    ComputeQuotaReadExtended,
    ComputeQuotaReadExtendedPublic,
)
from app.service.models import ComputeService
from app.tests.utils.compute_quota import create_random_compute_quota
from app.tests.utils.utils import random_lower_string
from pydantic import ValidationError


def test_create_schema():
    """Create a valid 'Create' Schema."""
    create_random_compute_quota(project=uuid4())
    create_random_compute_quota(default=True, project=uuid4())


def test_invalid_create_schema():
    """List all invalid situations for a 'Create' Schema."""
    a = create_random_compute_quota(project=uuid4())
    with pytest.raises(ValidationError):
        a.type = QuotaType.BLOCK_STORAGE.value
    with pytest.raises(ValidationError):
        a.type = random_lower_string()
    with pytest.raises(ValidationError):
        a.project = None
    with pytest.raises(ValidationError):
        a.cores = -1
    with pytest.raises(ValidationError):
        a.fixed_ips = -1
    with pytest.raises(ValidationError):
        a.public_ips = -1
    with pytest.raises(ValidationError):
        a.instances = -1
    with pytest.raises(ValidationError):
        a.ram = -1


def test_read_schema(db_compute_serv: ComputeService):
    """Create a valid 'Read' Schema."""
    db_region = db_compute_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]

    obj_in = create_random_compute_quota(project=db_project.uuid)
    db_obj = compute_quota.create(
        obj_in=obj_in, service=db_compute_serv, project=db_project
    )
    ComputeQuotaRead.from_orm(db_obj)
    ComputeQuotaReadPublic.from_orm(db_obj)
    ComputeQuotaReadShort.from_orm(db_obj)
    ComputeQuotaReadExtended.from_orm(db_obj)
    ComputeQuotaReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_compute_quota(default=True, project=db_project.uuid)
    db_obj = compute_quota.update(
        db_obj=db_obj, obj_in=obj_in, projects=db_provider.projects, force=True
    )
    ComputeQuotaRead.from_orm(db_obj)
    ComputeQuotaReadPublic.from_orm(db_obj)
    ComputeQuotaReadShort.from_orm(db_obj)
    ComputeQuotaReadExtended.from_orm(db_obj)
    ComputeQuotaReadExtendedPublic.from_orm(db_obj)
