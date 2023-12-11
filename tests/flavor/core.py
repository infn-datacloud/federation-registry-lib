"""Module to test Flavor schema creation."""
from typing import Any, Dict
from uuid import uuid4

from tests.utils.utils import (
    random_bool,
    random_lower_string,
    random_non_negative_int,
    random_positive_int,
)


class Core:
    """Core Class for a Flavor.

    Defines dictionaries used to create Flavor instances.
    """

    @property
    def mandatory_kwargs(self) -> Dict[str, Any]:
        """Dict with Flavor mandatory attributes."""
        return {"name": random_lower_string(), "uuid": uuid4()}

    @property
    def all_kwargs(self) -> Dict[str, Any]:
        """Dict with all Flavor attributes."""
        return {
            **self.mandatory_kwargs,
            "is_public": random_bool(),
            "description": random_lower_string(),
            "disk": random_non_negative_int(),
            "ram": random_non_negative_int(),
            "vcpus": random_non_negative_int(),
            "swap": random_non_negative_int(),
            "ephemeral": random_non_negative_int(),
            "infiniband": random_bool(),
            "gpus": random_positive_int(),
            "gpu_model": random_lower_string(),
            "gpu_vendor": random_lower_string(),
            "local_storage": random_lower_string(),
        }
