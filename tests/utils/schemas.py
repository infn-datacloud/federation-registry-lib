from abc import ABC, abstractmethod
from datetime import date
from typing import Any, Dict, Generic, Optional, Type, TypeVar

from neomodel import StructuredNode
from pydantic import BaseModel

from app.models import BaseNode, BaseNodeCreate
from tests.utils.utils import random_lower_string

ModelType = TypeVar("ModelType", bound=StructuredNode)
BasicSchemaType = TypeVar("BasicSchemaType", bound=BaseNode)
BasicPublicSchemaType = TypeVar("BasicPublicSchemaType", bound=BaseNode)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseNodeCreate)


class SchemaBase(
    ABC,
    Generic[
        ModelType,
        BasicSchemaType,
        BasicPublicSchemaType,
        CreateSchemaType,
        UpdateSchemaType,
    ],
):
    def __init__(
        self,
        *,
        base_schema: Type[BasicSchemaType],
        base_public_schema: Type[BasicPublicSchemaType],
        create_schema: Type[CreateSchemaType],
        update_schema: Type[UpdateSchemaType],
    ) -> None:
        super().__init__()
        self.base_public_schema = base_public_schema
        self.base_schema = base_schema
        self.create_schema = create_schema
        self.update_schema = update_schema

    @abstractmethod
    def random_create_extended_item(self, **kwargs) -> CreateSchemaType:
        return self.create_schema(**kwargs)

    @abstractmethod
    def random_patch_item(
        self, *, default: bool = False, from_item: Optional[ModelType] = None, **kwargs
    ) -> UpdateSchemaType:
        if default:
            return self.update_schema()
        if from_item:
            d = {
                k: from_item.__getattribute__(k)
                for k in self.base_schema.__fields__.keys()
            }
            return self.update_schema(**d)
        return self.update_schema(description=random_lower_string(), **kwargs)

    @abstractmethod
    def _validate_read_relationships(
        self, *, obj: Dict[str, Any], db_item: ModelType, public: bool = False
    ) -> None:
        pass

    @abstractmethod
    def _validate_create_relationships(
        self, *, obj: Dict[str, Any], db_item: ModelType
    ) -> None:
        pass

    def _validate_attrs(
        self, *, obj: Dict[str, Any], db_item: ModelType, public: bool = False
    ) -> None:
        if public:
            attrs = self.base_public_schema.__fields__
        else:
            attrs = self.base_schema.__fields__
        for attr in attrs:
            db_attr = db_item.__getattribute__(attr)
            if isinstance(db_attr, date):
                db_attr = db_attr.isoformat()
            assert db_attr == obj.pop(attr, None)

    def _validate_create_attrs(
        self, *, obj: Dict[str, Any], db_item: ModelType
    ) -> None:
        self._validate_attrs(obj=obj, db_item=db_item, public=False)
        self._validate_create_relationships(obj=obj, db_item=db_item)
        assert not obj

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
            self._validate_read_relationships(obj=obj, db_item=db_item, public=public)
        assert not obj
