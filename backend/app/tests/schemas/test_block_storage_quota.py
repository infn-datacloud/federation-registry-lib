from uuid import uuid4

import pytest
from app.quota.crud import block_storage_quota
from app.quota.enum import QuotaType
from app.quota.schemas import (
    BlockStorageQuotaRead,
    BlockStorageQuotaReadPublic,
    BlockStorageQuotaReadShort,
)
from app.quota.schemas_extended import (
    BlockStorageQuotaReadExtended,
    BlockStorageQuotaReadExtendedPublic,
)
from app.service.models import BlockStorageService
from app.tests.utils.quota import create_random_block_storage_quota
from app.tests.utils.utils import random_lower_string
from pydantic import ValidationError


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
        a.type = random_lower_string()
    with pytest.raises(ValidationError):
        a.project = None
    with pytest.raises(ValidationError):
        a.gigabytes = -2
    with pytest.raises(ValidationError):
        a.per_volume_gigabytes = -2
    with pytest.raises(ValidationError):
        a.volumes = -2


def test_read_schema(db_block_storage_serv: BlockStorageService):
    """Create a valid 'Read' Schema."""
    db_region = db_block_storage_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]

    obj_in = create_random_block_storage_quota(project=db_project.uuid)
    db_obj = block_storage_quota.create(
        obj_in=obj_in, service=db_block_storage_serv, project=db_project
    )
    BlockStorageQuotaRead.from_orm(db_obj)
    BlockStorageQuotaReadPublic.from_orm(db_obj)
    BlockStorageQuotaReadShort.from_orm(db_obj)
    BlockStorageQuotaReadExtended.from_orm(db_obj)
    BlockStorageQuotaReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_block_storage_quota(default=True, project=db_project.uuid)
    db_obj = block_storage_quota.update(
        db_obj=db_obj, obj_in=obj_in, projects=db_provider.projects, force=True
    )
    BlockStorageQuotaRead.from_orm(db_obj)
    BlockStorageQuotaReadPublic.from_orm(db_obj)
    BlockStorageQuotaReadShort.from_orm(db_obj)
    BlockStorageQuotaReadExtended.from_orm(db_obj)
    BlockStorageQuotaReadExtendedPublic.from_orm(db_obj)
