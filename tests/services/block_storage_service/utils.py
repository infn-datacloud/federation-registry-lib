"""BlockStorageService utilitiees."""
from random import choice
from typing import Any, Dict

from app.service.enum import BlockStorageServiceName
from tests.common.utils import random_lower_string, random_url


def random_block_storage_service_required_attr() -> Dict[str, Any]:
    """Dict with BlockStorageService mandatory attributes."""
    return {"endpoint": random_url(), "name": random_block_storage_service_name()}


def random_block_storage_service_all_attr() -> Dict[str, Any]:
    """Dict with all BlockStorageService attributes."""
    return {
        **random_block_storage_service_required_attr(),
        "description": random_lower_string(),
    }


def random_block_storage_service_name() -> str:
    """Return one of the possible BlockStorageService names."""
    return choice([i.value for i in BlockStorageServiceName])
