"""Module to test Flavor schema creation."""
from typing import Any, Dict
from uuid import uuid4

from pytest_cases import parametrize

from tests.utils.utils import (
    random_bool,
    random_lower_string,
    random_non_negative_int,
    random_positive_int,
)

is_public = {True, False}
is_extended = {True, False}
gpu_details = {
    ("gpu_model", random_lower_string()),  # gpus is 0
    ("gpu_vendor", random_lower_string()),  # gpus is 0
}
invalid_create_key_values = {
    ("uuid", None),
    ("name", None),
    ("disk", -1),
    ("ram", -1),
    ("vcpus", -1),
    ("swap", -1),
    ("ephemeral", -1),
} | gpu_details
patch_key_values = {
    ("uuid", uuid4()),
    ("name", random_lower_string()),
    ("description", random_lower_string()),
    ("disk", random_non_negative_int()),
    ("ram", random_non_negative_int()),
    ("vcpus", random_non_negative_int()),
    ("swap", random_non_negative_int()),
    ("ephemeral", random_non_negative_int()),
    ("infiniband", random_bool()),
    ("gpus", random_positive_int()),
    ("local_storage", random_lower_string()),
    ("uuid", None),
    ("name", None),
    ("local_storage", None),
}
invalid_patch_key_values = {
    ("description", None),
    ("disk", None),
    ("ram", None),
    ("vcpus", None),
    ("swap", None),
    ("ephemeral", None),
    ("infiniband", None),
    ("gpus", None),
} | gpu_details
invalid_patch_gpu_details = {}
relationships_num = {0, 1, 2}


class ValidCreateData:
    """Valid data for create schemas."""

    @parametrize("is_public", is_public)
    def case_valid_data_default(
        self, is_public: bool, data_mandatory: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Valid set of Flavor mandatory attributes and relationships."""
        kwargs = {**data_mandatory}
        if not is_public:
            kwargs["is_public"] = is_public
            kwargs["projects"] = [uuid4()]
        return kwargs

    def case_valid_data(self, data_all: Dict[str, Any]) -> Dict[str, Any]:
        """Valid set of Flavor attributes and relationships."""
        kwargs = {**data_all}
        if not kwargs["is_public"]:
            kwargs["projects"] = [uuid4()]
        return kwargs


class InvalidCreateData:
    """Invalid data for create schemas."""

    @parametrize("k, v", invalid_create_key_values)
    def case_invalid_key_values(
        self, k: str, v: Any, data_mandatory: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Invalid set of Flavor attributes."""
        kwargs = {**data_mandatory}
        kwargs[k] = v
        return kwargs

    @parametrize("is_public", is_public)
    def case_invalid_projects_list_size(
        self, is_public: bool, data_mandatory: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Invalid project list size.

        Invalid cases: If flavor is marked as public, the list has at least one element,
        if private, the list has no items.
        """
        kwargs = {**data_mandatory}
        kwargs["is_public"] = is_public
        kwargs["projects"] = None if not is_public else [uuid4()]
        return kwargs

    def case_duplicated_projects(
        self, data_mandatory: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Invalid case: the project list has duplicate values."""
        project_uuid = uuid4()
        kwargs = {**data_mandatory}
        kwargs["is_public"] = False
        kwargs["projects"] = [project_uuid, project_uuid]
        return kwargs


class ReadSchemaVisibility:
    """Class for public/private cases."""

    @parametrize("public", is_public)
    def case_public_schema(self, public: bool) -> bool:
        """Return True if the schema is the public one."""
        return public


class ReadSchemaConnection:
    """Class for extended/short cases."""

    @parametrize("extended", is_extended)
    def case_extended_schema(self, extended: bool) -> bool:
        """Return True if the schema is the extended one."""
        return extended


class ValidPatchData:
    """Data to execute patch operations."""

    @parametrize("k, v", patch_key_values)
    def case_patch_single_attribute(self, k: str, v: Any) -> Dict[str, Any]:
        """Dict with single key-value pair to update."""
        return {k: v}

    @parametrize("k, v", gpu_details)
    def case_gpu_details(self, k: str, v: Any) -> Dict[str, Any]:
        """Invalid set of Flavor attributes."""
        return {"gpus": random_positive_int(), k: v}


class InvalidPatchData:
    """Invalid data to create Patch object."""

    @parametrize("k, v", invalid_patch_key_values)
    def case_invalid_key_values(self, k: str, v: Any) -> Dict[str, Any]:
        """Invalid set of Flavor attributes."""
        return {k: v}
