from typing import Any, Dict, Generic, Type, TypeVar

from neomodel import StructuredNode
from pydantic import BaseModel

from app.models import BaseNode

ModelType = TypeVar("ModelType", bound=StructuredNode)
BasicSchemaType = TypeVar("BasicSchemaType", bound=BaseNode)
BasicPublicSchemaType = TypeVar("BasicPublicSchemaType", bound=BaseNode)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class SchemaCreation:
    def _random_patch_item(self, *, default: bool = False) -> None:
        pass


class SchemaValidation(
    SchemaCreation, Generic[ModelType, BasicSchemaType, BasicPublicSchemaType]
):
    def __init__(
        self,
        *,
        base_schema: Type[BasicSchemaType],
        base_public_schema: Type[BasicPublicSchemaType],
    ) -> None:
        super().__init__()
        self.base_schema = base_schema
        self.base_public_schema = base_public_schema

    def _validate_attrs(
        self, *, obj: Dict[str, Any], db_item: ModelType, public: bool = False
    ) -> None:
        if public:
            attrs = self.base_public_schema.__fields__
        else:
            attrs = self.base_schema.__fields__
        for attr in attrs:
            assert db_item.__getattribute__(attr) == obj.pop(attr, None)

    def _validate_relationships(
        self, *, obj: Dict[str, Any], db_item: ModelType, public: bool = False
    ) -> None:
        pass

    def _validate_read_attrs(
        self,
        *,
        obj: Dict[str, Any],
        db_item: ModelType,
        public: bool = False,
        extended: bool = False,
    ) -> None:
        assert db_item.uid == obj.pop("uid", None)
        self._validate_attrs(obj=obj, db_item=db_item, public=public)
        if extended:
            self._validate_relationships(obj=obj, db_item=db_item, public=public)
        assert not obj
