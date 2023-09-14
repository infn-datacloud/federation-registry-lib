import os
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
from models.config import URLs
from pydantic import UUID4, AnyHttpUrl, BaseModel

WriteSchema = TypeVar("WriteSchema", bound=BaseModel)
ReadSchema = TypeVar("ReadSchema", bound=BaseModel)


class BasicPopulation(Generic[WriteSchema, ReadSchema]):
    def __init__(
        self,
        *,
        type: str,
        write_schema: Type[WriteSchema],
        read_schema: Type[ReadSchema],
        get_url: AnyHttpUrl,
        post_url: AnyHttpUrl,
        patch_url: AnyHttpUrl,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        self.type = type.capitalize()
        self.write_schema = write_schema
        self.read_schema = read_schema
        self.get_url = get_url
        self.post_url = post_url
        self.patch_url = patch_url
        self.read_headers = read_headers
        self.write_headers = write_headers

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
        params: Optional[Dict[str, Any]] = None,
        parent_uid: Optional[UUID4] = None,
    ) -> ReadSchema:
        """Create new instance."""
        label = self._repr(item=new_data)
        logger.info(f"Creating new {self.type} '{label}'")
        url = self.post_url
        if parent_uid is not None:
            url = os.path.join(url, str(parent_uid), f"{self.type.lower()}s")
        resp = requests.post(
            url=self.post_url,
            json=jsonable_encoder(new_data),
            headers=self.write_headers,
            params=params,
        )
        if resp.status_code == status.HTTP_201_CREATED:
            logger.info(f"{self.type} '{label}' successfully created")
            return self.read_schema(**resp.json())
        else:
            self._action_failed(name=label, resp=resp, action="create")

    def update(
        self,
        *,
        new_data: WriteSchema,
        old_data: ReadSchema,
        uid: UUID4,
    ) -> ReadSchema:
        """Update existing instance."""
        label = self._repr(item=new_data)
        logger.info(f"Trying to update {self.type} '{label}'.")
        url = os.path.join(self.patch_url, str(uid))
        resp = requests.patch(
            url=url, json=jsonable_encoder(new_data), headers=self.write_headers
        )
        if resp.status_code == status.HTTP_200_OK:
            logger.info(f"{self.type} '{label}' successfully updated")
            return self.read_schema(**resp.json())
        elif resp.status_code == status.HTTP_304_NOT_MODIFIED:
            logger.info("New data match stored data.")
            logger.info(f"{self.type} '{label}' not modified")
            return old_data
        else:
            self._action_failed(name=label, resp=resp, action="update")

    def single(self, *, params: Dict[str, Any]) -> Optional[ReadSchema]:
        """Find instance with given params."""
        db_item = None
        resp = requests.get(url=self.get_url, params=params, headers=self.read_headers)
        if resp.status_code == status.HTTP_200_OK:
            if len(resp.json()) == 0:
                logger.info(f"{self.type} '{list(params.values())}' not found")
            elif len(resp.json()) == 1:
                logger.info(f"{self.type} '{list(params.values())}' found")
                db_item = self.read_schema(**resp.json()[0])
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
        get_url: AnyHttpUrl,
        post_url: AnyHttpUrl,
        patch_url: AnyHttpUrl,
        connect_url: AnyHttpUrl,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        self.connect_url = connect_url
        super().__init__(
            type=type,
            write_schema=write_schema,
            read_schema=read_schema,
            get_url=get_url,
            post_url=post_url,
            patch_url=patch_url,
            read_headers=read_headers,
            write_headers=write_headers,
        )

    def connect(
        self,
        *,
        parent_uid: UUID4,
        uid: UUID4,
        new_data: WriteSchema,
    ) -> None:
        label = self._repr(item=new_data)
        logger.info(f"Connecting {self.type} '{label}'.")
        data = None
        if new_data.dict().get("relationship") is not None:
            data = new_data.relationship
        url = self.connect_url
        if parent_uid is not None:
            url = os.path.join(url, str(parent_uid), f"{self.type.lower()}s")
        url = os.path.join(url, str(uid))
        resp = requests.put(
            url=url, headers=self.write_headers, json=jsonable_encoder(data)
        )
        if resp.status_code == status.HTTP_200_OK:
            logger.info(f"{self.type} '{label}' successfully connected")
        elif resp.status_code == status.HTTP_304_NOT_MODIFIED:
            logger.info(f"{self.type} '{label}' already connected. Data not modified")
        else:
            self._action_failed(name=label, resp=resp, action="connect")


class ImagePopulation(BasicPopulation[ImageWrite, ImageRead]):
    def __init__(
        self,
        get_url: AnyHttpUrl,
        post_url: AnyHttpUrl,
        patch_url: AnyHttpUrl,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            type="Image",
            read_schema=ImageRead,
            write_schema=ImageWrite,
            get_url=get_url,
            post_url=post_url,
            patch_url=patch_url,
            read_headers=read_headers,
            write_headers=write_headers,
        )


class FlavorPopulation(BasicPopulation[FlavorWrite, FlavorRead]):
    def __init__(
        self,
        get_url: AnyHttpUrl,
        post_url: AnyHttpUrl,
        patch_url: AnyHttpUrl,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            type="Flavor",
            read_schema=FlavorRead,
            write_schema=FlavorWrite,
            get_url=get_url,
            post_url=post_url,
            patch_url=patch_url,
            read_headers=read_headers,
            write_headers=write_headers,
        )


class ProjectPopulation(BasicPopulation[ProjectWrite, ProjectRead]):
    def __init__(
        self,
        get_url: AnyHttpUrl,
        post_url: AnyHttpUrl,
        patch_url: AnyHttpUrl,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            type="Project",
            read_schema=ProjectRead,
            write_schema=ProjectWrite,
            get_url=get_url,
            post_url=post_url,
            patch_url=patch_url,
            read_headers=read_headers,
            write_headers=write_headers,
        )


class ProviderPopulation(BasicPopulation[ProviderWrite, ProviderRead]):
    def __init__(
        self,
        get_url: AnyHttpUrl,
        post_url: AnyHttpUrl,
        patch_url: AnyHttpUrl,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            type="Provider",
            read_schema=ProviderRead,
            write_schema=ProviderWrite,
            get_url=get_url,
            post_url=post_url,
            patch_url=patch_url,
            read_headers=read_headers,
            write_headers=write_headers,
        )


class LocationPopulation(Connectable[LocationWrite, LocationRead]):
    def __init__(
        self,
        get_url: AnyHttpUrl,
        post_url: AnyHttpUrl,
        patch_url: AnyHttpUrl,
        connect_url: AnyHttpUrl,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            type="Location",
            read_schema=LocationRead,
            write_schema=LocationWrite,
            get_url=get_url,
            post_url=post_url,
            patch_url=patch_url,
            connect_url=connect_url,
            read_headers=read_headers,
            write_headers=write_headers,
        )


class IdentityProviderPopulation(
    Connectable[IdentityProviderWrite, IdentityProviderRead]
):
    def __init__(
        self,
        get_url: AnyHttpUrl,
        post_url: AnyHttpUrl,
        patch_url: AnyHttpUrl,
        connect_url: AnyHttpUrl,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            type="IdentityProvider",
            read_schema=IdentityProviderRead,
            write_schema=IdentityProviderWrite,
            get_url=get_url,
            post_url=post_url,
            patch_url=patch_url,
            connect_url=connect_url,
            read_headers=read_headers,
            write_headers=write_headers,
        )


class ServicePopulation(BasicPopulation[ServiceWrite, ServiceRead]):
    def __init__(
        self,
        get_url: AnyHttpUrl,
        post_url: AnyHttpUrl,
        patch_url: AnyHttpUrl,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            type="Service",
            read_schema=ServiceRead,
            write_schema=ServiceWrite,
            get_url=get_url,
            post_url=post_url,
            patch_url=patch_url,
            read_headers=read_headers,
            write_headers=write_headers,
        )


class QuotaPopulation(BasicPopulation[QuotaWrite, QuotaRead]):
    def __init__(
        self,
        get_url: AnyHttpUrl,
        post_url: AnyHttpUrl,
        patch_url: AnyHttpUrl,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            type="Quota",
            read_schema=QuotaRead,
            write_schema=QuotaWrite,
            get_url=get_url,
            post_url=post_url,
            patch_url=patch_url,
            read_headers=read_headers,
            write_headers=write_headers,
        )


class CRUDs:
    def __init__(
        self,
        cmdb_urls: URLs,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        self.flavors = FlavorPopulation(
            get_url=cmdb_urls.flavors,
            post_url=cmdb_urls.providers,
            patch_url=cmdb_urls.flavors,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.identity_providers = IdentityProviderPopulation(
            get_url=cmdb_urls.identity_providers,
            post_url=cmdb_urls.identity_providers,
            patch_url=cmdb_urls.identity_providers,
            connect_url=cmdb_urls.providers,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.images = ImagePopulation(
            get_url=cmdb_urls.images,
            post_url=cmdb_urls.providers,
            patch_url=cmdb_urls.images,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.locations = LocationPopulation(
            get_url=cmdb_urls.locations,
            post_url=cmdb_urls.locations,
            patch_url=cmdb_urls.locations,
            connect_url=cmdb_urls.providers,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.projects = ProjectPopulation(
            get_url=cmdb_urls.projects,
            post_url=cmdb_urls.providers,
            patch_url=cmdb_urls.projects,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.providers = ProviderPopulation(
            get_url=cmdb_urls.providers,
            post_url=cmdb_urls.providers,
            patch_url=cmdb_urls.providers,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.quotas = QuotaPopulation(
            get_url=cmdb_urls.quotas,
            post_url=cmdb_urls.quotas,
            patch_url=cmdb_urls.quotas,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.services = ServicePopulation(
            get_url=cmdb_urls.services,
            post_url=cmdb_urls.providers,
            patch_url=cmdb_urls.services,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        # slas = None
        # user_groups = None
