"""Module to test Flavor schema creation."""
from pytest_cases import case


class SchemaCases:
    """Create, Read and Patch data cases."""

    @case(tags="create_valid")
    def case_valid_create_schema(self, valid_create_schema_actors):
        """Valid data for create schemas."""
        return valid_create_schema_actors

    @case(tags="create_invalid")
    def case_invalid_key_values(self, invalid_create_schema_actors):
        """Invalid data for create schemas."""
        return invalid_create_schema_actors

    @case(tags="patch_valid")
    def case_valid_patch_schema(self, valid_patch_schema_actors):
        """Data to execute patch operations."""
        return valid_patch_schema_actors

    @case(tags="patch_invalid")
    def case_invalid_patch_schema(self, invalid_patch_schema_actors):
        """Invalid data to create Patch object."""
        return invalid_patch_schema_actors

    @case(tags="read")
    def case_read_schema(self, valid_read_schema_actors):
        """Class for public/private cases."""
        cls_name = valid_read_schema_actors[0].__name__
        is_public = False
        is_extended = False
        if "Public" in cls_name:
            is_public = True
        if "Extended" in cls_name:
            is_extended = True
        return (
            valid_read_schema_actors[0],
            valid_read_schema_actors[1],
            is_public,
            is_extended,
            valid_read_schema_actors[2],
        )
