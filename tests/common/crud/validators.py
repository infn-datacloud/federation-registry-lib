"""Module to test Flavor schema creation."""
from typing import Any, Dict, Generic, List, Optional, Type
from uuid import UUID

from pydantic.fields import SHAPE_LIST

from app.crud import CRUDBase
from tests.common.validators import (
    BasePublicType,
    BaseType,
    BaseValidation,
    CreateType,
    DbType,
)


class CreateOperationValidation(
    BaseValidation, Generic[BaseType, BasePublicType, CreateType, DbType]
):
    """Class with functions used to validate Create operations."""

    def __init__(
        self,
        *,
        base: Type[BaseType],
        base_public: Type[BasePublicType],
        create: Type[CreateType],
    ) -> None:
        """Define base, base public and create types.

        Args:
        ----
            base (type of BaseType): Schema class with public and private attributes.
            base_public (type of BasePublicType): Schema class with public attributes.
            create (type of CreateType): Schema class to create an instance.
        """
        super().__init__(base=base, base_public=base_public)
        self.create = create

    def _exclude_not_used_attrs(
        self, *, data: Dict[str, Any], exclude_attrs: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Do not consider not used attributes.

        Args:
        ----
            data (dict): Dict to filter.
            exclude_attrs (list of str): List of attributes marked as useless.

        Returns:
        -------
            The original data object without the attributes in exclude_attrs.
        """
        if exclude_attrs is None:
            exclude_attrs = []
        exclude_attrs.append("id")
        for i in exclude_attrs:
            data.pop(i, None)
        return data

    def validate_db_item_attrs(
        self,
        *,
        db_item: DbType,
        schema: CreateType,
        exclude_attrs: Optional[List[str]] = None,
    ) -> None:
        """Validate data attributes and relationships with the expected ones.

        Validate attributes and relationships.

        Args:
        ----
            db_item (DbType): Database instance with the created data. To be validated.
            schema (CreateType): Schema with the info to add to the database.
            exclude_attrs (list of str): List of attributes of the database model to
                ignore.
        """
        count = 0
        data = db_item.__dict__

        assert data.pop("uid")
        self.validate_attrs(data=data, schema=schema, public=False)

        attrs = self.create.__fields__.keys() - self.base.__fields__.keys()
        for attr in attrs:
            field = self.create.__fields__.get(attr)
            if field.shape == SHAPE_LIST:
                schema_list = schema.__getattribute__(attr)

                # Specific for Region instance
                if attr.endswith("services"):
                    count += 1
                    service_type = attr[: -len("service") - 2].replace("_", "-")
                    data_list = data.get("services", []).filter(type=service_type)
                    if count == 4:
                        data.pop("services", [])
                else:
                    data_list = data.pop(attr, [])

                assert len(schema_list) == len(data_list)

                if isinstance(field.type_, str):
                    schema_list = sorted([x.uuid for x in schema_list])
                    data_list: List[UUID] = sorted(data_list)
                    for schema_str, data_str in zip(schema_list, data_list):
                        assert schema_str == data_str.hex
                else:
                    pass
            else:
                if issubclass(field.type_, str):
                    v: UUID = data.pop(attr, None)
                    v = v.hex if v else v
                    assert schema.__getattribute__(attr) == v
                else:
                    # We do not check this part since nested items checks are duplicates
                    # of other specific tests. We only pop the item if present.
                    data.pop(attr, None)

        data = self._exclude_not_used_attrs(data=data, exclude_attrs=exclude_attrs)
        assert not data


class ReadOperationValidation(
    BaseValidation, Generic[BaseType, BasePublicType, DbType]
):
    """Class with functions used to validate Read operations."""

    def validate_retrieved_item(
        self, *, db_item: DbType, retrieved_item: DbType
    ) -> None:
        """Validate data attributes and relationships with the expected ones.

        Validate attributes and relationships.

        Args:
        ----
            db_item (DbType): Database instance.
            retrieved_item (DbType): Retrieved data. To be validated.
        """
        for k in self.base.__fields__.keys():
            assert db_item.__dict__.get(k) == retrieved_item.__dict__.get(k)


class DeleteOperationValidation(
    BaseValidation, Generic[BaseType, BasePublicType, DbType]
):
    """Class with functions used to validate Delete operations."""

    def __init__(
        self,
        *,
        base: Type[BaseType],
        base_public: Type[BasePublicType],
        managers: Dict[str, CRUDBase],
    ) -> None:
        """Define base, base public and create types.

        Store the managers that will be used to check children deletion.

        Args:
        ----
            base (type of BaseType): Schema class with public and private attributes.
            base_public (type of BasePublicType): Schema class with public attributes.
            managers (dict): the key is the relationship name, the value is the manager.
        """
        super().__init__(base=base, base_public=base_public)
        self.managers = managers

    def validate_deleted_children(self, *, db_item: DbType) -> None:
        """Validate that target item and children entities have been deleted.

        Args:
        ----
            db_item (DbType): Deleted database instance.
        """
        for k in self.managers:
            if k.endswith("services"):
                service_type = k[: -len("service") - 2].replace("_", "-")
                items = db_item.__getattribute__("services").filter(type=service_type)
            else:
                items = db_item.__getattribute__(k).all()
            for i in items:
                assert not self.managers[k].get(uid=i.uid)


class PatchOperationValidation(
    BaseValidation, Generic[BaseType, BasePublicType, DbType]
):
    """Class with functions used to validate Patch operations."""

    def validate_updated_item(
        self, *, old_item: DbType, updated_item: DbType, new_data: Dict[str, Any]
    ) -> None:
        """Check that updated data match old data and new data."""
        old_data = old_item.__dict__
        updated_data = updated_item.__dict__
        for k in self.base.__fields__.keys():
            old_val = old_data.pop(k, None)
            new_val = updated_data.pop(k, None)
            if k in new_data.keys():
                assert new_data[k] == new_val
            else:
                assert old_val == new_val
