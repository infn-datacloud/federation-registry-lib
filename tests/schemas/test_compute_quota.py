from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.quota.enum import QuotaType
from app.quota.models import ComputeQuota
from app.quota.schemas import (
    ComputeQuotaRead,
    ComputeQuotaReadPublic,
    ComputeQuotaReadShort,
)
from app.quota.schemas_extended import (
    ComputeQuotaReadExtended,
    ComputeQuotaReadExtendedPublic,
)
from tests.utils.compute_quota import (
    create_random_compute_quota,
    validate_read_compute_quota_attrs,
    validate_read_extended_compute_quota_attrs,
    validate_read_extended_public_compute_quota_attrs,
    validate_read_public_compute_quota_attrs,
    validate_read_short_compute_quota_attrs,
)
from tests.utils.utils import random_lower_string


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
        a.type = QuotaType.NETWORK.value
    with pytest.raises(ValidationError):
        a.type = random_lower_string()
    with pytest.raises(ValidationError):
        a.project = None
    with pytest.raises(ValidationError):
        a.cores = -1
    with pytest.raises(ValidationError):
        a.instances = -1
    with pytest.raises(ValidationError):
        a.ram = -1


def test_read_schema(db_compute_quota: ComputeQuota):
    """Create a valid 'Read' Schema."""
    schema = ComputeQuotaRead.from_orm(db_compute_quota)
    validate_read_compute_quota_attrs(obj_out=schema, db_item=db_compute_quota)
    schema = ComputeQuotaReadShort.from_orm(db_compute_quota)
    validate_read_short_compute_quota_attrs(obj_out=schema, db_item=db_compute_quota)
    schema = ComputeQuotaReadPublic.from_orm(db_compute_quota)
    validate_read_public_compute_quota_attrs(obj_out=schema, db_item=db_compute_quota)
    schema = ComputeQuotaReadExtended.from_orm(db_compute_quota)
    validate_read_extended_compute_quota_attrs(obj_out=schema, db_item=db_compute_quota)
    schema = ComputeQuotaReadExtendedPublic.from_orm(db_compute_quota)
    validate_read_extended_public_compute_quota_attrs(
        obj_out=schema, db_item=db_compute_quota
    )
