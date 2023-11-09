from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.quota.enum import QuotaType
from app.quota.models import NetworkQuota
from app.quota.schemas import (
    NetworkQuotaRead,
    NetworkQuotaReadPublic,
    NetworkQuotaReadShort,
)
from app.quota.schemas_extended import (
    NetworkQuotaReadExtended,
    NetworkQuotaReadExtendedPublic,
)
from tests.utils.network_quota import (
    create_random_network_quota,
    validate_read_extended_network_quota_attrs,
    validate_read_extended_public_network_quota_attrs,
    validate_read_network_quota_attrs,
    validate_read_public_network_quota_attrs,
    validate_read_short_network_quota_attrs,
)
from tests.utils.utils import random_lower_string


def test_create_schema():
    """Create a valid 'Create' Schema."""
    create_random_network_quota(project=uuid4())
    create_random_network_quota(default=True, project=uuid4())


def test_invalid_create_schema():
    """List all invalid situations for a 'Create' Schema."""
    a = create_random_network_quota(project=uuid4())
    with pytest.raises(ValidationError):
        a.type = QuotaType.BLOCK_STORAGE.value
    with pytest.raises(ValidationError):
        a.type = QuotaType.COMPUTE.value
    with pytest.raises(ValidationError):
        a.type = random_lower_string()
    with pytest.raises(ValidationError):
        a.project = None
    with pytest.raises(ValidationError):
        a.public_ips = -2
    with pytest.raises(ValidationError):
        a.networks = -2
    with pytest.raises(ValidationError):
        a.ports = -2
    with pytest.raises(ValidationError):
        a.security_groups = -2
    with pytest.raises(ValidationError):
        a.security_group_rules = -2


def test_read_schema(db_network_quota: NetworkQuota):
    """Create a valid 'Read' Schema."""
    schema = NetworkQuotaRead.from_orm(db_network_quota)
    validate_read_network_quota_attrs(obj_out=schema, db_item=db_network_quota)
    schema = NetworkQuotaReadShort.from_orm(db_network_quota)
    validate_read_short_network_quota_attrs(obj_out=schema, db_item=db_network_quota)
    schema = NetworkQuotaReadPublic.from_orm(db_network_quota)
    validate_read_public_network_quota_attrs(obj_out=schema, db_item=db_network_quota)
    schema = NetworkQuotaReadExtended.from_orm(db_network_quota)
    validate_read_extended_network_quota_attrs(obj_out=schema, db_item=db_network_quota)
    schema = NetworkQuotaReadExtendedPublic.from_orm(db_network_quota)
    validate_read_extended_public_network_quota_attrs(
        obj_out=schema, db_item=db_network_quota
    )
