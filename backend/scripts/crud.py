from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

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
    QuotaRead,
    QuotaWrite,
    ServiceRead,
    ServiceWrite,
)
from pydantic import AnyHttpUrl, BaseModel

WriteSchema = TypeVar("WriteSchema", bound=BaseModel)
ReadSchema = TypeVar("ReadSchema", bound=BaseModel)


class BasicPopulation(Generic[WriteSchema, ReadSchema]):
    def __init__(
        self,
        *,
        type: str,
        write_schema: Type[WriteSchema],
        read_schema: Type[ReadSchema],
    ) -> None:
        self.type = type.capitalize()
        self.write_schema = write_schema
        self.read_schema = read_schema

    def _repr(self, *, item: WriteSchema) -> str:
        if item.dict().get("name") is not None:
            return item.name
        if item.dict().get("endpoint") is not None:
            return item.endpoint

    def _action_failed(
        self, *, resp: requests.Response, name: str, action: str
    ) -> None:
        logger.error(f"Failed to {action} {self.type.lower()} '{name}'")
        logger.error(f"Status code: {resp.status_code}")
        logger.error(f"Message: {resp.text}")
        raise BaseException("Operation failed")

    def create(
        self,
        *,
        new_data: WriteSchema,
        url: AnyHttpUrl,
        header: Dict[str, str],
        params: Optional[Dict[str, Any]] = None,
    ) -> ReadSchema:
        """Create new instance."""
        label = self._repr(item=new_data)
        resp = requests.post(
            url=url, json=jsonable_encoder(new_data), headers=header, params=params
        )
        if resp.status_code == status.HTTP_201_CREATED:
            logger.info(f"{self.type} '{label}' successfully created")
            return self.read_schema.parse_obj(resp.json())
        else:
            self._action_failed(name=label, resp=resp, action="create")

    def update(
        self, *, new_data: WriteSchema, url: AnyHttpUrl, header: Dict[str, str]
    ) -> Optional[ReadSchema]:
        """Update existing instance."""
        label = self._repr(item=new_data)
        resp = requests.patch(url=url, json=jsonable_encoder(new_data), headers=header)
        if resp.status_code == status.HTTP_200_OK:
            logger.info(f"{self.type} '{label}' successfully updated")
            return self.read_schema.parse_obj(resp.json())
        elif resp.status_code == status.HTTP_304_NOT_MODIFIED:
            logger.info("New data match stored data.")
            logger.info(f"{self.type} '{label}' not modified")
        else:
            self._action_failed(name=label, resp=resp, action="update")

    def find(
        self, *, url: AnyHttpUrl, header: Dict[str, str], params: Dict[str, Any]
    ) -> Optional[ReadSchema]:
        """Find instance with given params."""
        db_item = None
        resp = requests.get(url=url, params=params, headers=header)
        if resp.status_code == status.HTTP_200_OK:
            if len(resp.json()) == 0:
                logger.info(f"{self.type} '{list(params.values())}' not found")
            elif len(resp.json()) == 1:
                logger.info(f"{self.type} '{list(params.values())}' found")
                db_item = self.read_schema.parse_obj(resp.json()[0])
            else:
                logger.error(
                    f"{self.type} '{list(params.values())}' multiple occurrences found"
                )
                raise Exception("Database corrupted")
        else:
            self._action_failed(name=list(params.values()), resp=resp, action="find")
        return db_item

    def find_in_list(
        self, *, key: str, value: str, db_items: List[ReadSchema]
    ) -> Optional[ReadSchema]:
        """Find instance within a given list with corresponding key-value
        pair."""
        items = [i.dict().get(key) for i in db_items]
        if value in items:
            logger.info(f"{self.type} '{value}' already belongs to this provider")
            idx = items.index(value)
            return db_items[idx]
        logger.info(f"No {self.type.lower()}s '{value}' belongs to this provider.")
        return None


class Connectable(BasicPopulation[WriteSchema, ReadSchema]):
    def __init__(
        self,
        *,
        type: str,
        write_schema: Type[WriteSchema],
        read_schema: Type[ReadSchema],
    ) -> None:
        super().__init__(type=type, write_schema=write_schema, read_schema=read_schema)

    def connect(
        self, *, url: AnyHttpUrl, header: Dict[str, str], new_data: WriteSchema
    ) -> None:
        label = self._repr(item=new_data)
        data = None
        if new_data.dict().get("relationship") is not None:
            data = new_data.relationship
        resp = requests.put(url=url, headers=header, json=jsonable_encoder(data))
        if resp.status_code == status.HTTP_200_OK:
            logger.info(f"{self.type} '{label}' successfully connected")
        elif resp.status_code == status.HTTP_304_NOT_MODIFIED:
            logger.info(f"{self.type} '{label}' already connected. Data not modified")
        else:
            self._action_failed(name=label, resp=resp, action="connect")


class ImagePopulation(BasicPopulation[ImageWrite, ImageRead]):
    def __init__(self) -> None:
        super().__init__(type="Image", read_schema=ImageRead, write_schema=ImageWrite)


class FlavorPopulation(BasicPopulation[FlavorWrite, FlavorRead]):
    def __init__(self) -> None:
        super().__init__(
            type="Flavor", read_schema=FlavorRead, write_schema=FlavorWrite
        )


class ProjectPopulation(BasicPopulation[ProjectWrite, ProjectRead]):
    def __init__(self) -> None:
        super().__init__(
            type="Project", read_schema=ProjectRead, write_schema=ProjectWrite
        )


class ProviderPopulation(BasicPopulation[ProviderWrite, ProviderRead]):
    def __init__(self) -> None:
        super().__init__(
            type="Provider", read_schema=ProviderRead, write_schema=ProviderWrite
        )


class LocationPopulation(Connectable[LocationWrite, LocationRead]):
    def __init__(self) -> None:
        super().__init__(
            type="Location", read_schema=LocationRead, write_schema=LocationWrite
        )


class IdentityProviderPopulation(
    Connectable[IdentityProviderWrite, IdentityProviderRead]
):
    def __init__(self) -> None:
        super().__init__(
            type="IdentityProvider",
            read_schema=IdentityProviderRead,
            write_schema=IdentityProviderWrite,
        )


class ServicePopulation(BasicPopulation[ServiceWrite, ServiceRead]):
    def __init__(self) -> None:
        super().__init__(
            type="Service",
            read_schema=ServiceRead,
            write_schema=ServiceWrite,
        )


class QuotaPopulation(BasicPopulation[QuotaWrite, QuotaRead]):
    def __init__(self) -> None:
        super().__init__(
            type="Quota",
            read_schema=QuotaRead,
            write_schema=QuotaWrite,
        )
