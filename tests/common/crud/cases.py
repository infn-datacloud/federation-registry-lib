"""Module with possible cases to test create, read, update and delete operation."""
from typing import Literal

from pytest_cases import case, parametrize


class CRUDCases:
    """Create, Read and Patch data cases."""

    @case(tags="create_item")
    def case_create_item(self, create_item_actors):
        """Valid data for create schemas."""
        return create_item_actors

    # TODO create invalid?

    @case(tags="read_single")
    def case_read_single_item(self, valid_read_item_actors):
        """Class for public/private cases."""
        return valid_read_item_actors

    @case(tags="read_multi")
    def case_read_multi_items(self, valid_read_items_actors):
        """Class for public/private cases."""
        return valid_read_items_actors

    @case(tags="not_existing")
    def case_manager(self, not_existing_actors):
        """Class for public/private cases."""
        return not_existing_actors

    @case(tags="delete")
    def case_delete_item(self, delete_item_actors):
        """Class for public/private cases."""
        return delete_item_actors

    @case(tags="patch")
    def case_patch_item(self, patch_item_actors):
        """Class for public/private cases."""
        return patch_item_actors

    @case(tags="patch")
    def case_patch_item_with_default(self, patch_item_with_default_actors):
        """Class for public/private cases."""
        return patch_item_with_default_actors

    @case(tags="patch_required_with_none")
    def case_patch_required_with_none(self, patch_item_required_with_none_actors):
        """Class for public/private cases."""
        return patch_item_required_with_none_actors

    @case(tags="patch_no_changes")
    def case_patch_no_changes_item(self, patch_item_no_changes_actors):
        """Class for public/private cases."""
        return patch_item_no_changes_actors

    @case(tags="force_update")
    def case_force_update_unchanged_rel_item(self, force_update_unchanged_rel_actors):
        """Class for public/private cases."""
        return force_update_unchanged_rel_actors

    @case(tags="force_update")
    def case_force_update_add_rel_item(self, force_update_add_rel_actors):
        """Class for public/private cases."""
        return force_update_add_rel_actors

    @case(tags="force_update")
    def case_force_update_remove_rel_item(self, force_update_remove_rel_actors):
        """Class for public/private cases."""
        return force_update_remove_rel_actors

    @case(tags="force_update")
    def case_force_update_replace_rel_item(self, force_update_replace_rel_actors):
        """Class for public/private cases."""
        return force_update_replace_rel_actors


class GetParams:
    """Cases with the possible parameters that can be passed to a CRUD read request."""

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
