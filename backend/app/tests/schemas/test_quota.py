import pytest
from app.quota.enum import QuotaType
from app.tests.utils.quota import (
    create_random_block_storage_quota,
    create_random_compute_quota,
)
from pydantic import ValidationError


def test_create_schema():
    create_random_block_storage_quota()
    create_random_block_storage_quota(default=True)

    create_random_compute_quota()
    create_random_compute_quota(default=True)


def test_invalid_create_schema():
    a = create_random_block_storage_quota()
    with pytest.raises(ValidationError):
        a.type = QuotaType.COMPUTE.value
    with pytest.raises(ValidationError):
        a.project = None
    with pytest.raises(ValidationError):
        a.gigabytes = -1
    with pytest.raises(ValidationError):
        a.per_volume_gigabytes = -1
    with pytest.raises(ValidationError):
        a.volumes = -1

    a = create_random_compute_quota()
    with pytest.raises(ValidationError):
        a.type = QuotaType.BLOCK_STORAGE.value
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
