"""Module with possible cases to test create, read, update and delete operation."""
from typing import Literal

from pytest_cases import case, parametrize


class CRUDCases:
    """Create, Read and Patch data cases."""

    @case(tags="create_item")
    def case_create_item(self, create_item_tuple):
        """Valid data for create schemas."""
        return create_item_tuple

    # @case(tags="create_invalid")
    # def case_invalid_key_values(self, invalid_create_schema_tuples):
    #     """Invalid data for create schemas."""
    #     return invalid_create_schema_tuples

    # @case(tags="patch_valid")
    # def case_valid_patch_schema(self, valid_patch_schema_tuples):
    #     """Data to execute patch operations."""
    #     return valid_patch_schema_tuples

    # @case(tags="patch_invalid")
    # def case_invalid_patch_schema(self, invalid_patch_schema_tuples):
    #     """Invalid data to create Patch object."""
    #     return invalid_patch_schema_tuples

    @case(tags="read_single")
    def case_read_single_item(self, valid_read_item_tuples):
        """Class for public/private cases."""
        return valid_read_item_tuples

    @case(tags="read_multi")
    def case_read_multi_items(self, valid_read_items_tuples):
        """Class for public/private cases."""
        return valid_read_items_tuples

    @case(tags="not_existing")
    def case_manager(self, item_manager):
        """Class for public/private cases."""
        return item_manager

    @case(tags="delete")
    def case_delete_item(self, delete_item_tuples):
        """Class for public/private cases."""
        return delete_item_tuples


class GetParams:
    """Cases with the possible parameters that can be passed to a CRUD GET request."""

    @case(tags="single_attr")
    def case_attr(self, item_attr) -> str:
        """One of the possible attribute of this item."""
        return item_attr

    @case(tags="single_attr")
    def case_uid_attr(self) -> Literal["uid"]:
        """The 'uid' string."""
        return "uid"

    @case(tags="sort")
    @parametrize(reverse=[True, False])
    def case_sort(self, reverse: str, item_attr: str) -> int:
        """Direct and reverse sort order for a possible attribute of this item."""
        if reverse:
            return "-" + item_attr
        return item_attr

    @case(tags="limit")
    @parametrize(limit=[0, 1, 2, 3])
    def case_limit(self, limit: int) -> int:
        """Possible limit value."""
        return limit

    @case(tags="skip")
    @parametrize(skip=[0, 1, 2])
    def case_skip(self, skip: int) -> int:
        """Possible skip value."""
        return skip

    @case(tags=["single_attr", "limit"])
    def case_no_attr(self) -> None:
        """Returns None."""
        return None
