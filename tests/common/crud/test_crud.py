"""Module to test Schemas creation, patch and read."""
import copy
from uuid import uuid4

import pytest
from neomodel import RequiredProperty
from pytest_cases import parametrize_with_cases

CASES = [
    # "tests.flavor.cases_crud",
    # "tests.identity_provider.cases_crud",
    # "tests.image.cases_crud",
    # "tests.location.cases_crud",
    # "tests.network.cases_crud",
    # "tests.project.cases_crud",
    "tests.provider.cases_crud",
    # "tests.quotas.block_storage_quota.cases_crud",
    # "tests.quotas.compute_quota.cases_crud",
    # "tests.quotas.network_quota.cases_crud",
    # "tests.region.cases_crud",
    # "tests.services.block_storage_service.cases_crud",
    # "tests.services.compute_service.cases_crud",
    # "tests.services.identity_service.cases_crud",
    # "tests.services.network_service.cases_crud",
    # "tests.sla.cases_crud",
    # "tests.user_group.cases_crud",
]


class TestCRUD:
    """Test create, update, delete and read operations.

    Test delete not existing is not implemented because the API already block delete
    operations on not existing items.
    # TODO test failing creation?
    """

    @parametrize_with_cases(
        "manager, validator, schema, kwargs", cases=CASES, has_tag="create_item"
    )
    def test_create(self, manager, validator, schema, kwargs) -> None:
        """Test create operation.

        From a CreateSchema execute the create operation and validate the attributes of
        the created item.
        """
        db_item = manager.create(obj_in=schema, **kwargs)
        validator.validate_db_item_attrs(
            db_item=db_item, schema=schema, exclude_attrs=list(kwargs.keys())
        )

    @parametrize_with_cases("manager", cases=CASES, has_tag="not_existing")
    def test_read_single_not_existing(self, manager) -> None:
        """Create a schema from a dict."""
        retrieved_item = manager.get(uid=uuid4())
        assert not retrieved_item

    @parametrize_with_cases(
        "manager, validator, db_item, attr", cases=CASES, has_tag="read_single"
    )
    def test_read_single(self, manager, validator, db_item, attr) -> None:
        """Create a schema from a dict."""
        kwargs = {attr: db_item.__getattribute__(attr)} if attr else {}
        retrieved_item = manager.get(**kwargs)
        validator.validate_retrieved_item(
            db_item=db_item, retrieved_item=retrieved_item
        )

    @parametrize_with_cases("manager", cases=CASES, has_tag="not_existing")
    def test_read_multi_not_existing(self, manager) -> None:
        """Create a schema from a dict."""
        retrieved_items = manager.get_multi(uid=uuid4())
        assert isinstance(retrieved_items, list)
        assert len(retrieved_items) == 0

    @parametrize_with_cases(
        "manager, validator, db_items, attr", cases=CASES, has_tag="read_multi"
    )
    def test_read_multi_specific_attr(self, manager, validator, db_items, attr) -> None:
        """Create a schema from a dict."""
        target_item = db_items[0]
        kwargs = {attr: target_item.__getattribute__(attr)} if attr else {}
        retrieved_items = manager.get_multi(**kwargs)
        assert isinstance(retrieved_items, list)

        if len(retrieved_items) > 1:
            retrieved_items = list(
                filter(lambda x: x.uid == target_item.uid, retrieved_items)
            )
        validator.validate_retrieved_item(
            db_item=target_item, retrieved_item=retrieved_items[0]
        )

    @parametrize_with_cases(
        "manager, validator, db_items, attr", cases=CASES, has_tag="sort"
    )
    def test_read_multi_sort(self, manager, validator, db_items, attr) -> None:
        """Create a schema from a dict."""
        retrieved_items = manager.get_multi(sort=attr)
        assert isinstance(retrieved_items, list)

        sorted_retrieved_items = retrieved_items
        if attr.startswith("-"):
            sorted_db_items = sorted(
                db_items, key=lambda x: x.__getattribute__(attr[1:]), reverse=True
            )
        else:
            sorted_db_items = sorted(db_items, key=lambda x: x.__getattribute__(attr))
        assert len(sorted_db_items) == len(sorted_retrieved_items)

        for db_item, retrieved_item in zip(sorted_db_items, sorted_retrieved_items):
            validator.validate_retrieved_item(
                db_item=db_item, retrieved_item=retrieved_item
            )

    @parametrize_with_cases(
        "manager, validator, db_items, attr", cases=CASES, has_tag="limit"
    )
    def test_read_multi_limit(self, manager, validator, db_items, attr) -> None:
        """Create a schema from a dict."""
        retrieved_items = manager.get_multi(sort="uid", limit=attr)
        assert isinstance(retrieved_items, list)

        sorted_retrieved_items = retrieved_items
        sorted_db_items = sorted(db_items, key=lambda x: x.uid)[:attr]
        assert len(sorted_db_items) == len(sorted_retrieved_items)

        for db_item, retrieved_item in zip(sorted_db_items, sorted_retrieved_items):
            validator.validate_retrieved_item(
                db_item=db_item, retrieved_item=retrieved_item
            )

    @parametrize_with_cases(
        "manager, validator, db_items, attr", cases=CASES, has_tag="skip"
    )
    def test_read_multi_skip(self, manager, validator, db_items, attr) -> None:
        """Create a schema from a dict."""
        retrieved_items = manager.get_multi(sort="uid", skip=attr)
        assert isinstance(retrieved_items, list)

        sorted_retrieved_items = retrieved_items
        sorted_db_items = sorted(db_items, key=lambda x: x.uid)[attr:]
        assert len(sorted_db_items) == len(sorted_retrieved_items)

        for db_item, retrieved_item in zip(sorted_db_items, sorted_retrieved_items):
            validator.validate_retrieved_item(
                db_item=db_item, retrieved_item=retrieved_item
            )

    @parametrize_with_cases(
        "manager, validator, db_item", cases=CASES, has_tag="delete"
    )
    def test_delete(self, manager, validator, db_item) -> None:
        """The schema creation fails and raises an error."""
        old_item = copy.deepcopy(db_item)
        assert manager.remove(db_obj=db_item)
        assert not manager.get(uid=db_item.uid)
        validator.validate_deleted_children(db_item=old_item)

    @parametrize_with_cases(
        "manager, validator, db_item, new_data", cases=CASES, has_tag="patch"
    )
    def test_patch(self, manager, validator, db_item, new_data) -> None:
        """The schema creation fails and raises an error."""
        old_item = copy.deepcopy(db_item)
        updated_item = manager.update(db_obj=db_item, obj_in=new_data)
        validator.validate_updated_item(
            old_item=old_item,
            updated_item=updated_item,
            new_data=new_data.dict(exclude_unset=True),
        )

    @parametrize_with_cases(
        "manager, db_item, new_data", cases=CASES, has_tag="patch_required_with_none"
    )
    def test_patch_required_with_none(self, manager, db_item, new_data) -> None:
        """The schema creation fails and raises an error."""
        with pytest.raises(RequiredProperty):
            manager.update(db_obj=db_item, obj_in=new_data)

    @parametrize_with_cases(
        "manager, db_item, new_data", cases=CASES, has_tag="patch_no_changes"
    )
    def test_patch_no_changes(self, manager, db_item, new_data) -> None:
        """The schema creation fails and raises an error."""
        assert not manager.update(db_obj=db_item, obj_in=new_data)

    @parametrize_with_cases(
        "manager, validator, db_item, new_data", cases=CASES, has_tag="force_update"
    )
    def test_force_update(self, manager, validator, db_item, new_data) -> None:
        """The schema creation fails and raises an error."""
        old_item = copy.deepcopy(db_item)
        updated_item = manager.update(db_obj=db_item, obj_in=new_data, force=True)
        validator.validate_updated_item(
            old_item=old_item,
            updated_item=updated_item,
            new_data=new_data.dict(exclude_unset=True),
        )
        # TODO validate relationships.
        # relationships = (
        #     self.read_extended.__fields__.keys() - self.base.__fields__.keys()
        # )
        # relationships.remove("uid")
        # for k in relationships:
        #     old_val = old_data.pop(k, None)
        #     new_val = updated_data.pop(k, None)
        #     if k in new_data.keys():
        #         assert new_data[k] == new_val
        #     else:
        #         assert len(old_val) == len(new_val)
        #         old_val = sorted([i.uid for i in old_val.all()], key=lambda x: x.uid)
        #         new_val = sorted([i.uid for i in new_val.all()], key=lambda x: x.uid)
        #         for i, j in zip(old_val, new_val):
        #             assert i == j
