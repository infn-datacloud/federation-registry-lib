import pytest
from app.tests.utils.region import create_random_region
from pydantic import ValidationError


def test_create_schema():
    create_random_region()
    create_random_region(default=True)
    create_random_region(with_location=True)
    create_random_region(default=True, with_location=True)
    create_random_region(with_block_storage_services=True)
    create_random_region(default=True, with_block_storage_services=True)
    create_random_region(with_compute_services=True)
    create_random_region(default=True, with_compute_services=True)
    create_random_region(with_identity_services=True)
    create_random_region(default=True, with_identity_services=True)
    create_random_region(with_network_services=True)
    create_random_region(default=True, with_network_services=True)
    create_random_region(
        with_location=True,
        with_block_storage_services=True,
        with_compute_services=True,
        with_identity_services=True,
        with_network_services=True,
    )


def test_invalid_create_schema():
    a = create_random_region(
        with_location=True,
        with_block_storage_services=True,
        with_compute_services=True,
        with_identity_services=True,
        with_network_services=True,
    )
    with pytest.raises(ValidationError):
        a.name = None
    with pytest.raises(ValidationError):
        a.block_storage_services = [
            a.block_storage_services[0],
            a.block_storage_services[0],
        ]
    with pytest.raises(ValidationError):
        a.compute_services = [a.compute_services[0], a.compute_services[0]]
    with pytest.raises(ValidationError):
        a.identity_services = [a.identity_services[0], a.identity_services[0]]
    with pytest.raises(ValidationError):
        a.network_services = [a.network_services[0], a.network_services[0]]
