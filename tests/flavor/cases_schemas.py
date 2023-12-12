"""Module to test Flavor schema creation."""
from typing import Any, Dict, Type

from pytest_cases import case

from app.flavor.schemas import FlavorUpdate
from app.provider.schemas_extended import FlavorCreateExtended


class SchemaCases:
    """Create, Read and Patch data cases."""

    @case(tags="create_valid")
    def case_valid_create_schema(
        self, flavor_create_valid_data: Dict[str, Any], flavor_create_validator: Any
    ):
        """Valid data for create schemas."""
        return FlavorCreateExtended, flavor_create_validator, flavor_create_valid_data

    @case(tags="create_invalid")
    def case_invalid_key_values(self, flavor_create_invalid_data: Dict[str, Any]):
        """Invalid data for create schemas."""
        return FlavorCreateExtended, flavor_create_invalid_data

    @case(tags="patch_valid")
    def case_valid_patch_schema(
        self, flavor_patch_valid_data: Dict[str, Any], flavor_patch_validator: Any
    ):
        """Data to execute patch operations."""
        return FlavorUpdate, flavor_patch_validator, flavor_patch_valid_data

    @case(tags="patch_invalid")
    def case_invalid_patch_schema(self, flavor_patch_invalid_data: Dict[str, Any]):
        """Invalid data to create Patch object."""
        return FlavorUpdate, flavor_patch_invalid_data

    @case(tags="read")
    def case_read_schema(
        self, flavor_read_class: Type[Any], flavor_read_validator: Any, db_flavor: Any
    ):
        """Class for public/private cases."""
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
