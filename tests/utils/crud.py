import copy
from typing import Dict, Generator, List, Optional, Type
from uuid import uuid4

import pytest

from app.crud import CRUDBase
from tests.utils.schemas import (
    BasicPublicSchemaType,
    BasicSchemaType,
    CreateSchemaType,
    ModelType,
    SchemaBase,
    UpdateSchemaType,
)

CRUD_PARAMS_MULTIPLE_ITEMS = [
    {},
    {"sort": "uid"},
    {"sort": "-uid"},
    {"sort": "uid", "limit": 0},
    {"sort": "uid", "limit": 1},
    {"sort": "uid", "limit": 2},
    {"sort": "uid", "skip": 0},
    {"sort": "uid", "skip": 1},
    {"sort": "uid", "skip": 2},
]


class BaseCRUD(
    SchemaBase[
        ModelType,
        BasicSchemaType,
        BasicPublicSchemaType,
        CreateSchemaType,
        UpdateSchemaType,
    ]
):
    def __init__(
        self,
        *,
        base_schema: Type[BasicSchemaType],
        base_public_schema: Type[BasicPublicSchemaType],
        create_schema: Type[CreateSchemaType],
        update_schema: Type[UpdateSchemaType],
        crud: CRUDBase,
    ) -> None:
        super().__init__(
            base_schema=base_schema,
            base_public_schema=base_public_schema,
            create_schema=create_schema,
            update_schema=update_schema,
        )
        self.crud = crud

    def create(self, *, default: bool = False, **kwargs) -> None:
        item_in = self.random_create_extended_item(default=default)
        item = self.crud.create(obj_in=item_in, **kwargs)
        self._validate_create_attrs(obj=item_in.dict(), db_item=item)

    def read(self, *, db_item: Optional[ModelType] = None, **kwargs) -> None:
        item = self.crud.get(**kwargs)
        if not db_item:
            assert not item
        else:
            relationships = list(item.__all_relationships__)
            item = item.__dict__
            item.pop("id")
            for rel in relationships:
                item.pop(rel[0])
            self._validate_read_attrs(
                obj=item, db_item=db_item, public=False, extended=False
            )

    def read_multi(
        self,
        *,
        db_items: Optional[List[ModelType]] = None,
        params: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> None:
        if not db_items:
            db_items = []

        sorted_items = self.crud.get_multi(**params, **kwargs)

        db_sorted_items = list(sorted(db_items, key=lambda x: x.uid))
        if not params.get("sort"):
            sorted_items = sorted(sorted_items, key=lambda x: x.uid)
        elif params.get("sort").startswith("-"):
            db_sorted_items.reverse()

        if params.get("limit") is not None:
            db_sorted_items = db_sorted_items[: params.get("limit")]
        if params.get("skip") is not None:
            db_sorted_items = db_sorted_items[params.get("skip") :]
        assert len(sorted_items) == len(db_sorted_items)

        for obj, db_item in zip(sorted_items, db_sorted_items):
            relationships = list(obj.__all_relationships__)
            obj = obj.__dict__
            obj.pop("id")
            for rel in relationships:
                obj.pop(rel[0])
            self._validate_read_attrs(
                obj=obj, db_item=db_item, public=False, extended=False
            )

    def patch(self, *, db_item: ModelType, new_data: UpdateSchemaType) -> None:
        return self.crud.update(db_obj=db_item, obj_in=new_data)


class TestBaseCRUD:
    __test__ = False
    controller: str
    db_item1: str
    db_item2: str
    db_parent1: str
    create_key_params: Dict

    @pytest.mark.parametrize("default", [False, True])
    def test_create_item(self, request: pytest.FixtureRequest, default: bool) -> None:
        """Create an item."""
        crud: BaseCRUD = request.getfixturevalue(self.controller)
        params = {}
        for k, v in self.create_key_params.items():
            params[v] = request.getfixturevalue(self.__getattribute__(k))
        crud.create(default=default, **params)

    # def test_create_item_private(db_compute_serv: ComputeService) -> None:
    #     """Create a private Flavor belonging to a specific Compute Service.

    #     Private Flavors requires a list of allowed projects.
    #     """
    #     db_region = db_compute_serv.region.single()
    #     db_provider = db_region.provider.single()
    #     item_in = create_random_flavor(projects=[i.uuid for i in db_provider.projects]
    # )
    #     item = flavor.create(
    #         obj_in=item_in, service=db_compute_serv, projects=db_provider.projects
    #     )
    #     validate_create_flavor_attrs(obj_in=item_in, db_item=item)

    # def test_create_item_with_same_uuid_diff_provider(
    #     db_compute_serv: ComputeService, db_compute_serv2: ComputeService
    # ) -> None:
    #     """Create a public Flavor belonging to a specific Compute Service.

    #     Connect a Flavor with the same UUID to another Provider. This operation is
    # allowed
    #     since the flavors belong to different providers.
    #     """
    #     item_in = create_random_flavor()
    #     item = flavor.create(obj_in=item_in, service=db_compute_serv)
    #     validate_create_flavor_attrs(obj_in=item_in, db_item=item)
    #     item2 = flavor.create(obj_in=item_in, service=db_compute_serv2)
    #     validate_create_flavor_attrs(obj_in=item_in, db_item=item)
    #     assert item.uid != item2.uid

    # def test_connect_same_item_to_different_service(
    #     db_compute_serv2: ComputeService, db_compute_serv3: ComputeService
    # ) -> None:
    #     """Create a public Flavor belonging to a specific Compute Service.

    #     Connect this same Flavor to another Compute Service of the same Provider. This
    #     operation is performed creating again the same flavor but passing another
    # service.
    #     """
    #     item_in = create_random_flavor()
    #     item = flavor.create(obj_in=item_in, service=db_compute_serv2)
    #     validate_create_flavor_attrs(obj_in=item_in, db_item=item)
    #     item2 = flavor.create(obj_in=item_in, service=db_compute_serv3)
    #     validate_create_flavor_attrs(obj_in=item_in, db_item=item)
    #     assert item.uid == item2.uid

    def test_read_item(self, request: pytest.FixtureRequest) -> None:
        """Retrieve an item from its UID."""
        crud: BaseCRUD = request.getfixturevalue(self.controller)
        db_item = request.getfixturevalue(self.db_item1)
        crud.read(db_item=db_item, uid=db_item.uid)

    def test_read_non_existing_item(
        self,
        request: pytest.FixtureRequest,
        setup_and_teardown_db: Generator,
    ) -> None:
        """Try to retrieve a not existing item."""
        crud: BaseCRUD = request.getfixturevalue(self.controller)
        crud.read(uid=uuid4())

    @pytest.mark.parametrize("params", CRUD_PARAMS_MULTIPLE_ITEMS)
    def test_read_items(
        self, request: pytest.FixtureRequest, params: Optional[Dict[str, str]]
    ) -> None:
        """Retrieve multiple Flavors."""
        crud: BaseCRUD = request.getfixturevalue(self.controller)
        crud.read_multi(
            db_items=[
                request.getfixturevalue(self.db_item1),
                request.getfixturevalue(self.db_item2),
            ],
            params=params,
        )

    @pytest.mark.parametrize("params", CRUD_PARAMS_MULTIPLE_ITEMS)
    def test_read_items_no_entries(
        self, request: pytest.FixtureRequest, params: Optional[Dict[str, str]]
    ) -> None:
        """Execute GET operations to read all items. But there are no items.

        Execute this operation using both authenticated and not-authenticated clients.
        """
        crud: BaseCRUD = request.getfixturevalue(self.controller)
        crud.read_multi(params=params)

    def test_read_item_with_target_params(self, request: pytest.FixtureRequest) -> None:
        """Execute GET operations to read all items matching specific attributes.

        Execute this operation using both authenticated and not-authenticated clients.
        """
        crud: BaseCRUD = request.getfixturevalue(self.controller)
        keys = list(crud.base_schema.__fields__.keys())
        keys.append("uid")

        db_item1 = request.getfixturevalue(self.db_item1)
        db_item2 = request.getfixturevalue(self.db_item2)
        for k in keys:
            v = db_item1.__getattribute__(k)
            db_items = [db_item1]
            if db_item2.__getattribute__(k) == v:
                db_items.append(db_item2)
            crud.read_multi(db_items=db_items, params={k: v})

    def test_patch_item(self, request: pytest.FixtureRequest) -> None:
        """Update the attributes of an existing Flavor, without updating its
        relationships.
        """
        crud: BaseCRUD = request.getfixturevalue(self.controller)
        db_item = request.getfixturevalue(self.db_item1)
        new_data = crud.random_patch_item()
        item = crud.patch(db_item=db_item, new_data=new_data)
        for k, v in new_data.dict().items():
            assert item.__getattribute__(k) == v

    def test_patch_item_no_edit(self, request: pytest.FixtureRequest) -> None:
        """Execute PATCH operations to update a specific item.

        New item attributes are the same as the existing one.
        No changes. The endpoint returns a 304 message.
        """
        crud: BaseCRUD = request.getfixturevalue(self.controller)
        db_item = request.getfixturevalue(self.db_item1)
        new_data = crud.random_patch_item(from_item=db_item)
        assert not crud.patch(db_item=db_item, new_data=new_data)

    def test_patch_item_empty_obj(self, request: pytest.FixtureRequest) -> None:
        """Try to update the attributes of an existing Flavor, without updating its
        relationships, with default values.

        Unset default values are discarded.
        """
        crud: BaseCRUD = request.getfixturevalue(self.controller)
        db_item = request.getfixturevalue(self.db_item1)
        new_data = crud.random_patch_item(default=True)
        assert not crud.patch(db_item=db_item, new_data=new_data)

    def test_patch_item_with_defaults(self, request: pytest.FixtureRequest) -> None:
        """Try to update the attributes of an existing Flavor, without updating its
        relationships, with default values.

        Specifying the default values, the operation succeeds.
        """
        crud: BaseCRUD = request.getfixturevalue(self.controller)
        db_item = request.getfixturevalue(self.db_item1)
        default_new_data = crud.random_patch_item(default=True)
        for attr, details in crud.base_schema.__fields__.items():
            new_data = copy.deepcopy(default_new_data)
            if not details.required:
                new_data.__setattr__(attr, details.default)
                item = crud.patch(db_item=db_item, new_data=new_data)
                # If item is None, no edit has been applied.
                # Otherwise check correctness.
                if item:
                    assert item.__getattribute__(attr) == new_data.__getattribute__(
                        attr
                    )
                    for k, v in db_item.__dict__.items():
                        if k != attr:
                            assert item.__getattribute__(k) == v
                else:
                    assert db_item.__getattribute__(attr) == new_data.__getattribute__(
                        attr
                    )
            # TODO To fix this behavior. Avoid to set to None required properties in
            # CRUDBase
            # else:
            #     new_data.__setattr__(attr, details.default)
            #     with pytest.raises(RequiredProperty):
            #         item = crud.patch(db_item=db_item, new_data=new_data)

    # TODO try to patch flavor setting it as private when there are no projects
    # or public when it has related projects


# def test_change_flavor_from_private_to_public(db_private_flavor: Flavor) -> None:
#     """Update the attributes and relationships of an existing Flavor.

#     Update a Flavor with a set of linked projects, updating its attributes and
# removing
#     all linked projects. Change it from private to public.
#     """
#     item_in = create_random_flavor()
#     item = flavor.update(db_obj=db_private_flavor, obj_in=item_in, force=True)
#     validate_create_flavor_attrs(obj_in=item_in, db_item=item)


# def test_change_flavor_from_public_to_private(db_public_flavor: Flavor) -> None:
#     """Update the attributes and relationships of an existing Flavor.

#     Update a Flavor with no projects, changing its attributes and linking a new
# project.
#     Change it from public to private.
#     """
#     db_service = db_public_flavor.services.single()
#     db_region = db_service.region.single()
#     db_provider = db_region.provider.single()
#     item_in = create_random_flavor(projects=[i.uuid for i in db_provider.projects])
#     item = flavor.update(
#         db_obj=db_public_flavor,
#         obj_in=item_in,
#         projects=db_provider.projects,
#         force=True,
#     )
#     validate_create_flavor_attrs(obj_in=item_in, db_item=item)


# def test_replace_private_flavor_projects(db_private_flavor: Flavor) -> None:
#     """Update the attributes and relationships of an existing Flavor.

#     Update a Flavor with a set of linked projects, changing both its attributes and
#     replacing the linked projects with new ones.
#     """
#     db_project = db_private_flavor.projects.single()
#     db_provider = db_project.provider.single()
#     item_in = create_random_flavor(projects=[i.uuid for i in db_provider.projects])
#     item = flavor.update(
#         db_obj=db_private_flavor,
#         obj_in=item_in,
#         projects=db_provider.projects,
#         force=True,
#     )
#     validate_create_flavor_attrs(obj_in=item_in, db_item=item)


# def test_force_update_without_changing_relationships(db_private_flavor: Flavor) ->
# None:
#     """Update the attributes and relationships of an existing Flavor.

#     Update a Flavor with a set of linked projects, changing only its attributes
# leaving
#     untouched its connections (this is different from the previous test because the
# flag
#     force is set to True).
#     """
#     db_projects = sorted(db_private_flavor.projects, key=lambda x: x.uid)
#     db_services = sorted(db_private_flavor.services, key=lambda x: x.uid)
#     item_in = create_random_flavor(
#         projects=[i.uuid for i in db_private_flavor.projects]
#     )
#     item = flavor.update(db_obj=db_private_flavor, obj_in=item_in, force=True)
#     validate_create_flavor_attrs(obj_in=item_in, db_item=item)
#     for i, j in zip(sorted(item.projects, key=lambda x: x.uid), db_projects):
#         assert i == j
#     for i, j in zip(sorted(item.services, key=lambda x: x.uid), db_services):
#         assert i == j


# def test_delete_item(db_public_flavor: Flavor) -> None:
#     """Delete an existing public Flavor."""
#     db_service = db_public_flavor.services.single()
#     assert flavor.remove(db_obj=db_public_flavor)
#     assert not flavor.get(uid=db_public_flavor.uid)
#     assert compute_service.get(uid=db_service.uid)


# def test_delete_item_with_relationships(db_private_flavor: Flavor) -> None:
#     """Delete an existing private Flavor.

#     Do not delete linked projects
#     """
#     db_service = db_private_flavor.services.single()
#     db_project = db_private_flavor.projects.single()
#     assert flavor.remove(db_obj=db_private_flavor)
#     assert not flavor.get(uid=db_private_flavor.uid)
#     assert project.get(uid=db_project.uid)
#     assert compute_service.get(uid=db_service.uid)
