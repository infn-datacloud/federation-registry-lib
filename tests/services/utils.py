"""Services utilities."""
from random import choice

from app.service.enum import (
    BlockStorageServiceName,
    ComputeServiceName,
    IdentityServiceName,
    NetworkServiceName,
)


def random_block_storage_service_name() -> str:
    """Return one of the possible BlockStorageService names."""
    return choice([i.value for i in BlockStorageServiceName])


def random_compute_service_name() -> str:
    """Return one of the possible ComputeService names."""
    return choice([i.value for i in ComputeServiceName])


def random_identity_service_name() -> str:
    """Return one of the possible IdentityService names."""
    return choice([i.value for i in IdentityServiceName])


def random_network_service_name() -> str:
    """Return one of the possible NetworkService names."""
    return choice([i.value for i in NetworkServiceName])
