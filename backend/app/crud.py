from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from neomodel import StructuredNode
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=StructuredNode)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)
ReadPublicSchemaType = TypeVar("ReadPublicSchemaType", bound=BaseModel)
ReadShortSchemaType = TypeVar("ReadShortSchemaType", bound=BaseModel)
ReadExtendedSchemaType = TypeVar("ReadExtendedSchemaType", BaseModel, None)
ReadExtendedPublicSchemaType = TypeVar("ReadExtendedPublicSchemaType", BaseModel, None)


class CRUDBase(
    Generic[
        ModelType,
        CreateSchemaType,
        UpdateSchemaType,
        ReadSchemaType,
        ReadPublicSchemaType,
        ReadShortSchemaType,
        ReadExtendedSchemaType,
        ReadExtendedPublicSchemaType,
    ]
):
    def __init__(
        self,
        *,
        model: Type[ModelType],
        create_schema: Type[CreateSchemaType],
        read_schema: Type[ReadSchemaType],
        read_public_schema: Type[ReadPublicSchemaType],
        read_short_schema: Type[ReadShortSchemaType],
        read_extended_schema: Type[ReadExtendedSchemaType],
        read_extended_public_schema: Type[ReadExtendedPublicSchemaType],
    ):
        """CRUD object with default methods to Create, Read, Update, Delete
        (CRUD)

        **Parameters**

        * `model`: A Neo4j model class
        * `create schema`: A Pydantic model (schema) class to create items
        * `read schema`: A Pydantic model (schema) class,
            for authenticated users, to read items
        * `read schema public`: A Pydantic model (schema) class,
            for unauthenticated users, to read items
        * `read schema short`: A Pydantic model (schema) class,
            for authenticated users, to read essential items' data
        * `read schema extended`: A Pydantic model (schema) class,
            for authenticated users, to read items with their connections
        """
        self.model = model
        self.create_schema = create_schema
        self.read_schema = read_schema
        self.read_public_schema = read_public_schema
        self.read_short_schema = read_short_schema
        self.read_extended_schema = read_extended_schema
        self.read_extended_public_schema = read_extended_public_schema

    def get(self, **kwargs) -> Optional[ModelType]:
        return self.model.nodes.get_or_none(**kwargs)

    def get_multi(
        self,
        *,
        skip: int = 0,
        limit: Optional[int] = None,
        sort: Optional[str] = None,
        **kwargs,
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

    def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in = self.create_schema.parse_obj(obj_in)
        obj_in_data = obj_in.dict(exclude_none=True)
        db_obj = None
        if db_obj is None:
            db_obj = self.model.create(obj_in_data)[0]
        return db_obj

    def update(
        self,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
        force: bool = False,
    ) -> Optional[ModelType]:
        obj_data = db_obj.__dict__
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=not force)

        if all([obj_data.get(k) == v for k, v in update_data.items()]):
            return None

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        return db_obj.save()

    def remove(self, *, db_obj: ModelType) -> bool:
        return db_obj.delete()

    def paginate(
        self, *, items: List[ModelType], page: int, size: Optional[int]
    ) -> List[ModelType]:
        if size is None:
            return items
        start = page * size
        end = start + size
        return items[start:end]

    def choose_out_schema(
        self, *, items: List[ModelType], auth: bool, short: bool, with_conn: bool
    ) -> Union[
        List[ReadPublicSchemaType],
        List[ReadShortSchemaType],
        List[ReadSchemaType],
        List[ReadExtendedPublicSchemaType],
        List[ReadExtendedSchemaType],
    ]:
        if auth:
            if with_conn:
                return [self.read_extended_schema.from_orm(i) for i in items]
            if short:
                return [self.read_short_schema.from_orm(i) for i in items]
            return [self.read_schema.from_orm(i) for i in items]
        if with_conn:
            return [self.read_extended_public_schema.from_orm(i) for i in items]
        return [self.read_public_schema.from_orm(i) for i in items]
