"""Module to test Flavor schema creation."""
from typing import Any, Dict, Type

from app.flavor.schemas import FlavorUpdate
from app.provider.schemas_extended import FlavorCreateExtended


class ValidCreateData:
    """Valid data for create schemas."""

    def case_valid_create_schema(
        self,
        flavor_create_valid_data: Dict[str, Any],
        flavor_create_validator,
    ):
        """Valid set of Flavor mandatory attributes and relationships."""
        return FlavorCreateExtended, flavor_create_validator, flavor_create_valid_data


class InvalidCreateData:
    """Invalid data for create schemas."""

    def case_invalid_key_values(self, flavor_create_invalid_data: Dict[str, Any]):
        """Invalid set of Flavor attributes."""
        return FlavorCreateExtended, flavor_create_invalid_data


class ValidPatchData:
    """Data to execute patch operations."""

    def case_valid_patch_schema(
        self,
        flavor_patch_valid_data: Dict[str, Any],
        flavor_patch_validator: Dict[str, Any],
    ):
        """Dict with single key-value pair to update."""
        return FlavorUpdate, flavor_patch_validator, flavor_patch_valid_data


class InvalidPatchData:
    """Invalid data to create Patch object."""

    def case_invalid_patch_schema(self, flavor_patch_invalid_data: Dict[str, Any]):
        """Invalid set of Flavor attributes."""
        return FlavorUpdate, flavor_patch_invalid_data


class ReadSchemaProperties:
    """Class for public/private cases."""

    def case_read_schema(
        self, flavor_read_class: Type[Any], flavor_read_validator: Any, db_flavor: Any
    ):
        """Return True if the schema is the public one."""
        cls_name = flavor_read_class.__name__
        is_public = False
        is_extended = False
        if "Public" in cls_name:
            is_public = True
        if "Extended" in cls_name:
            is_extended = True
        return (
            flavor_read_class,
            flavor_read_validator,
            is_public,
            is_extended,
            db_flavor,
        )
