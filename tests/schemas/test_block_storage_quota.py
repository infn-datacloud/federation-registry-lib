from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.quota.enum import QuotaType
from app.quota.models import BlockStorageQuota
from app.quota.schemas import (
    BlockStorageQuotaRead,
    BlockStorageQuotaReadPublic,
    BlockStorageQuotaReadShort,
)
from app.quota.schemas_extended import (
    BlockStorageQuotaReadExtended,
    BlockStorageQuotaReadExtendedPublic,
)
from tests.utils.block_storage_quota import (
    create_random_block_storage_quota,
    validate_read_block_storage_quota_attrs,
    validate_read_extended_block_storage_quota_attrs,
    validate_read_extended_public_block_storage_quota_attrs,
    validate_read_public_block_storage_quota_attrs,
    validate_read_short_block_storage_quota_attrs,
)
from tests.utils.utils import random_lower_string


def test_create_schema():
    """Create a valid 'Create' Schema."""
    create_random_block_storage_quota(project=uuid4())
    create_random_block_storage_quota(default=True, project=uuid4())


def test_invalid_create_schema():
    """List all invalid situations for a 'Create' Schema."""
    a = create_random_block_storage_quota(project=uuid4())
    with pytest.raises(ValidationError):
        a.type = QuotaType.COMPUTE.value
    with pytest.raises(ValidationError):
        a.type = QuotaType.NETWORK.value
    with pytest.raises(ValidationError):
        a.type = random_lower_string()
    with pytest.raises(ValidationError):
        a.project = None
    with pytest.raises(ValidationError):
        a.gigabytes = -2
    with pytest.raises(ValidationError):
        a.per_volume_gigabytes = -2
    with pytest.raises(ValidationError):
        a.volumes = -2


def test_read_schema(db_block_storage_quota: BlockStorageQuota):
    """Create a valid 'Read' Schema."""
    schema = BlockStorageQuotaRead.from_orm(db_block_storage_quota)
    validate_read_block_storage_quota_attrs(
        obj_out=schema, db_item=db_block_storage_quota
    )
    schema = BlockStorageQuotaReadShort.from_orm(db_block_storage_quota)
    validate_read_short_block_storage_quota_attrs(
        obj_out=schema, db_item=db_block_storage_quota
    )
    schema = BlockStorageQuotaReadPublic.from_orm(db_block_storage_quota)
    validate_read_public_block_storage_quota_attrs(
        obj_out=schema, db_item=db_block_storage_quota
    )
    schema = BlockStorageQuotaReadExtended.from_orm(db_block_storage_quota)
    validate_read_extended_block_storage_quota_attrs(
        obj_out=schema, db_item=db_block_storage_quota
    )
    schema = BlockStorageQuotaReadExtendedPublic.from_orm(db_block_storage_quota)
    validate_read_extended_public_block_storage_quota_attrs(
        obj_out=schema, db_item=db_block_storage_quota
    )
