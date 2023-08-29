from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from neomodel import StructuredNode
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=StructuredNode)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], schema: Type[CreateSchemaType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD)

        **Parameters**

        * `model`: A Neo4j model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.schema = schema

    def get(self, **kwargs) -> Optional[ModelType]:
        return self.model.nodes.get_or_none(**kwargs)

    def get_multi(
        self,
        *,
        skip: int = 0,
        limit: Optional[int] = None,
        sort: Optional[str] = None,
        **kwargs
    ) -> List[ModelType]:
        if kwargs:
            items = self.model.nodes.filter(**kwargs).order_by(sort).all()
        else:
            items = self.model.nodes.order_by(sort).all()

        if limit is None:
            return items[skip:]

        start = skip
        end = skip + limit
        return items[start:end]

    def create(
        self, *, obj_in: CreateSchemaType, force: bool = False
    ) -> ModelType:
        obj_in = self.schema.parse_obj(obj_in)
        obj_in_data = obj_in.dict(exclude_none=True)
        db_obj = None
        if not force:
            db_obj = self.model.nodes.get_or_none(**obj_in_data)
        if db_obj is None:
            db_obj = self.model.create(obj_in_data)[0]
        return db_obj

    def update(
        self,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> Optional[ModelType]:
        obj_data = db_obj.__dict__
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if all([obj_data[k] == v for k, v in update_data.items()]):
            return None

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        return db_obj.save()

    def remove(self, *, db_obj: ModelType) -> bool:
        return db_obj.delete()
