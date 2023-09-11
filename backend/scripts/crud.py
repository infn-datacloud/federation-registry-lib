import os
from typing import Dict, Generic, List, Optional, Tuple, TypeVar

import requests
from fastapi import status
from fastapi.encoders import jsonable_encoder
from logger import logger
from models.cmdb import (
    FlavorRead,
    FlavorWrite,
    IdentityProviderRead,
    IdentityProviderWrite,
    ImageRead,
    ImageWrite,
    LocationRead,
    LocationWrite,
    ProjectRead,
    ProjectWrite,
    ProviderRead,
    ProviderWrite,
)
from pydantic import AnyHttpUrl, BaseModel

WriteSchema = TypeVar("WriteSchema", bound=BaseModel)
ReadSchema = TypeVar("ReadSchema", bound=BaseModel)


class BasicPopulation(Generic[WriteSchema, ReadSchema]):
    def __init__(self, *, type: str, write_schema: str, read_schema: str) -> None:
        self.type = type.capitalize()
        self.write_schema = write_schema
        self.read_schema = read_schema

    def _action_failed(
        self, *, resp: requests.Response, name: str, action: str
    ) -> None:
        logger.error(f"Failed to {action} {self.type.lower()} '{name}'")
        logger.error(f"Status code: {resp.status_code}")
        logger.error(f"Message: {resp.text}")
        raise BaseException("Operation failed")

    def create(
        self, *, new_data: WriteSchema, url: AnyHttpUrl, header: Dict[str, str]
    ) -> ReadSchema:
        resp = requests.post(url=url, json=jsonable_encoder(new_data), headers=header)
        if resp.status_code == status.HTTP_201_CREATED:
            logger.info(f"{self.type} '{new_data.name}' successfully created")
            return self.read_schema.parse_obj(resp.json())
        else:
            self._action_failed(name=new_data.name, resp=resp, action="create")

    def update(
        self, *, new_data: WriteSchema, url: AnyHttpUrl, header: Dict[str, str]
    ) -> Optional[ReadSchema]:
        resp = requests.patch(url=url, json=jsonable_encoder(new_data), headers=header)
        if resp.status_code == status.HTTP_200_OK:
            logger.info(f"{self.type} '{new_data.name}' successfully updated")
            return self.read_schema.parse_obj(resp.json())
        elif resp.status_code == status.HTTP_304_NOT_MODIFIED:
            logger.info("New data match stored data.")
            logger.info(f"{self.type} '{new_data.name}' not modified")
        else:
            self._action_failed(name=new_data.name, resp=resp, action="update")


class UUIDNameFindable(
    BasicPopulation[WriteSchema, ReadSchema], Generic[WriteSchema, ReadSchema]
):
    def __init__(self, *, type: str, write_schema: str, read_schema: str) -> None:
        super().__init__(type=type, write_schema=write_schema, read_schema=read_schema)

    def find(
        self, *, new_data: WriteSchema, db_items: List[ReadSchema]
    ) -> Optional[ReadSchema]:
        db_item = None
        if new_data.name in [i.name for i in db_items]:
            idx = [i.name for i in db_items].index(new_data.name)
            db_item = db_items[idx]
            logger.info(
                f"{self.type} '{new_data.name}' already belongs to this provider"
            )
        elif new_data.uuid in [i.uuid for i in db_items]:
            idx = [i.uuid for i in db_items].index(new_data.uuid)
            db_item = db_items[idx]
            logger.info(
                f"{self.type} '{new_data.uuid}' already belongs to this provider"
            )
        else:
            logger.info(
                f"No {self.type.lower()}s with name '{new_data.name}' "
                f"or uuid '{new_data.uuid}' belongs to this provider"
            )
        return db_item


class FindableConnectable(BasicPopulation[WriteSchema, ReadSchema]):
    def __init__(self, *, type: str, write_schema: str, read_schema: str) -> None:
        super().__init__(type=type, write_schema=write_schema, read_schema=read_schema)

    def find(
        self,
        *,
        url: AnyHttpUrl,
        header: Dict[str, str],
        key_value_pair: Tuple[str, str],
    ) -> Optional[ReadSchema]:
        db_item = None
        resp = requests.get(
            url=url, params={key_value_pair[0]: key_value_pair[1]}, headers=header
        )
        if resp.status_code == status.HTTP_200_OK:
            if len(resp.json()) == 0:
                logger.info(f"{self.type} '{key_value_pair[1]}' not found")
            elif len(resp.json()) == 1:
                logger.info(f"{self.type} '{key_value_pair[1]}' found")
                db_item = self.read_schema.parse_obj(resp.json()[0])
            else:
                logger.error(
                    f"{self.type} '{key_value_pair[1]}' multiple occurrences found"
                )
                raise Exception("Database corrupted")
        else:
            self._action_failed(name=key_value_pair[1], resp=resp, action="find")
        return db_item

    def connect(
        self, *, url: AnyHttpUrl, header: Dict[str, str], new_data: ReadSchema
    ) -> None:
        url = os.path.join(url, str(new_data.uid))
        resp = requests.put(url=url, headers=header)
        if resp.status_code == status.HTTP_200_OK:
            logger.info(f"{self.type} '{new_data.name}' successfully connected")
        elif resp.status_code == status.HTTP_304_NOT_MODIFIED:
            logger.info(
                f"{self.type} '{new_data.name}' already connected. Data not modified"
            )
        else:
            self._action_failed(name=new_data.name, resp=resp, action="connect")


class ImagePopulation(UUIDNameFindable[ImageWrite, ImageRead]):
    def __init__(self) -> None:
        super().__init__(type="Image", read_schema=ImageRead, write_schema=ImageWrite)


class FlavorPopulation(UUIDNameFindable[FlavorWrite, FlavorRead]):
    def __init__(self) -> None:
        super().__init__(
            type="Flavor", read_schema=FlavorRead, write_schema=FlavorWrite
        )


class ProjectPopulation(UUIDNameFindable[ProjectWrite, ProjectRead]):
    def __init__(self) -> None:
        super().__init__(
            type="Project", read_schema=ProjectRead, write_schema=ProjectWrite
        )


class ProviderPopulation(BasicPopulation[ProviderWrite, ProviderRead]):
    def __init__(self) -> None:
        super().__init__(
            type="Provider", read_schema=ProviderRead, write_schema=ProviderWrite
        )


class LocationPopulation(FindableConnectable[LocationWrite, LocationRead]):
    def __init__(self) -> None:
        super().__init__(
            type="Location", read_schema=LocationRead, write_schema=LocationWrite
        )


class IdentityProviderPopulation(
    FindableConnectable[IdentityProviderWrite, IdentityProviderRead]
):
    def __init__(self) -> None:
        super().__init__(
            type="IdentityProvider",
            read_schema=IdentityProviderRead,
            write_schema=IdentityProviderWrite,
        )
