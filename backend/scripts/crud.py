import os
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

import requests
from fastapi import status
from fastapi.encoders import jsonable_encoder
from logger import logger
from models.cmdb import (
    FlavorQuery,
    FlavorRead,
    FlavorWrite,
    IdentityProviderQuery,
    IdentityProviderRead,
    IdentityProviderWrite,
    ImageQuery,
    ImageRead,
    ImageWrite,
    LocationQuery,
    LocationRead,
    LocationWrite,
    ProjectQuery,
    ProjectRead,
    ProjectWrite,
    ProviderQuery,
    ProviderRead,
    ProviderWrite,
    QuotaQuery,
    QuotaRead,
    QuotaWrite,
    ServiceQuery,
    ServiceRead,
    ServiceWrite,
)
from models.config import URLs
from pydantic import UUID4, AnyHttpUrl, BaseModel

ReadSchema = TypeVar("ReadSchema", bound=BaseModel)
QuerySchema = TypeVar("QuerySchema", bound=BaseModel)
WriteSchema = TypeVar("WriteSchema", bound=BaseModel)


class BasicCRUD(Generic[WriteSchema, ReadSchema, QuerySchema]):
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

    def _action_failed(
        self,
        *,
        resp: requests.Response,
        action: str,
        item: WriteSchema,
        name: Optional[str] = None,
    ) -> None:
        logger.error(f"Failed to {action} {item}")
        logger.error(f"Status code: {resp.status_code}")
        logger.error(f"Message: {resp.text}")
        raise BaseException("Failed to  failed")

    def create(
        self,
        *,
        new_data: WriteSchema,
        params: Optional[Dict[str, Any]] = None,
        parent_uid: Optional[UUID4] = None,
    ) -> ReadSchema:
        """Create new instance."""
        logger.info(f"Creating new {new_data}")
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
            logger.info(f"{new_data} successfully created")
            return self.read_schema(**resp.json())
        else:
            self._action_failed(resp=resp, action="create", item=new_data)

    def update(
        self,
        *,
        new_data: WriteSchema,
        old_data: ReadSchema,
    ) -> ReadSchema:
        """Update existing instance."""
        logger.info(f"Trying to update {new_data}.")
        url = os.path.join(self.patch_url, str(old_data.uid))
        resp = requests.patch(
            url=url, json=jsonable_encoder(new_data), headers=self.write_headers
        )
        if resp.status_code == status.HTTP_200_OK:
            logger.info(f"{new_data} successfully updated")
            return self.read_schema(**resp.json())
        elif resp.status_code == status.HTTP_304_NOT_MODIFIED:
            logger.info(f"New data match stored data. {new_data} not modified")
            return old_data
        else:
            self._action_failed(resp=resp, action="update", item=new_data)

    def single(
        self, *, data: QuerySchema, with_conn: bool = False
    ) -> Optional[ReadSchema]:
        """Find single instance with given params."""
        db_item = None
        resp = requests.get(
            url=self.get_url,
            params={**data.dict(exclude_unset=True), "with_conn": with_conn},
            headers=self.read_headers,
        )
        if resp.status_code == status.HTTP_200_OK:
            if len(resp.json()) == 0:
                logger.info(f"{data} not found")
            elif len(resp.json()) == 1:
                logger.info(f"{data} found")
                db_item = self.read_schema(**resp.json()[0])
            else:
                logger.error(f"{data} multiple occurrences found")
                raise Exception("Database corrupted")
        else:
            self._action_failed(resp=resp, action="find", item=data)
        return db_item

    def find_in_list(
        self, *, data: QuerySchema, db_items: List[ReadSchema]
    ) -> Optional[ReadSchema]:
        """Find instance within a given list with corresponding key-value
        pair."""
        data = data.dict(exclude_unset=True)
        for db_item in db_items:
            for k, v in data.items():
                if db_item.dict().get(k) == v:
                    logger.info(f"{data} already belongs to this provider")
                    return db_item
        logger.info(f"No {data} belongs to this provider.")
        return None

    def create_or_update(
        self,
        *,
        item: WriteSchema,
        db_item: Optional[ReadSchema] = None,
        parent_uid: Optional[UUID4] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> ReadSchema:
        """Create new item or update existing one."""
        if db_item is None:
            return self.create(new_data=item, parent_uid=parent_uid, params=params)
        return self.update(new_data=item, old_data=db_item)


class Connectable(BasicCRUD[WriteSchema, ReadSchema, QuerySchema]):
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

    def connect(self, *, new_data: WriteSchema, uid: UUID4, parent_uid: UUID4) -> None:
        """Connect item to another entity."""
        logger.info(f"Connecting {new_data}.")
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
            logger.info(f"{new_data} successfully connected")
        elif resp.status_code == status.HTTP_304_NOT_MODIFIED:
            logger.info(f"{new_data} already connected. Data not modified")
        else:
            self._action_failed(resp=resp, action="connect", item=new_data)


class FlavorCRUD(BasicCRUD[FlavorWrite, FlavorRead, FlavorQuery]):
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

    def create_or_update(
        self, *, item: FlavorWrite, parent: ProviderRead
    ) -> FlavorRead:
        db_item = self.find_in_list(
            data=FlavorQuery(name=item.name, uuid=item.uuid), db_items=parent.flavors
        )
        return super().create_or_update(
            item=item, db_item=db_item, parent_uid=parent.uid
        )


class IdentityProviderCRUD(
    Connectable[IdentityProviderWrite, IdentityProviderRead, IdentityProviderQuery]
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

    def create_or_update(
        self, *, item: IdentityProviderWrite, parent: ProviderRead
    ) -> IdentityProviderRead:
        db_item = self.single(data=IdentityProviderQuery(endpoint=item.endpoint))
        db_item = super().create_or_update(item=item, db_item=db_item)
        self.connect(new_data=item, uid=db_item.uid, parent_uid=parent.uid)
        return db_item


class ImageCRUD(BasicCRUD[ImageWrite, ImageRead, ImageQuery]):
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

    def create_or_update(self, *, item: ImageWrite, parent: ProviderRead) -> ImageRead:
        db_item = self.find_in_list(
            data=ImageQuery(name=item.name, uuid=item.uuid), db_items=parent.images
        )
        return super().create_or_update(
            item=item, db_item=db_item, parent_uid=parent.uid
        )


class LocationCRUD(Connectable[LocationWrite, LocationRead, LocationQuery]):
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

    def create_or_update(
        self, *, item: LocationWrite, parent: ProviderRead
    ) -> LocationRead:
        db_item = self.single(data=LocationQuery(name=item.name))
        db_item = super().create_or_update(item=item, db_item=db_item)
        self.connect(new_data=item, uid=db_item.uid, parent_uid=parent.uid)
        return db_item


class ProjectCRUD(BasicCRUD[ProjectWrite, ProjectRead, ProjectQuery]):
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

    def create_or_update(
        self, *, item: ProjectWrite, parent: ProviderRead
    ) -> ProjectRead:
        db_item = self.find_in_list(
            data=ProjectQuery(name=item.name, uuid=item.uuid), db_items=parent.projects
        )
        return super().create_or_update(
            item=item, db_item=db_item, parent_uid=parent.uid
        )


class ProviderCRUD(BasicCRUD[ProviderWrite, ProviderRead, ProviderQuery]):
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


class QuotaCRUD(BasicCRUD[QuotaWrite, QuotaRead, QuotaQuery]):
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

    def create_or_update(self, *, item: QuotaWrite, parent: ProjectRead) -> QuotaRead:
        db_item = self.find_in_list(
            data=QuotaQuery(name=item.type), db_items=parent.quotas
        )
        return super().create_or_update(
            item=item,
            db_item=db_item,
            params={
                "project_uid": parent.uid,
                "service_uid": item.service,
            },
        )


class ServiceCRUD(BasicCRUD[ServiceWrite, ServiceRead, ServiceQuery]):
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

    def create_or_update(
        self, *, item: ServiceWrite, parent: ProviderRead
    ) -> ServiceRead:
        db_item = self.find_in_list(
            data=ServiceQuery(name=item.name), db_items=parent.services
        )
        return super().create_or_update(
            item=item, db_item=db_item, parent_uid=parent.uid
        )


class CRUDs:
    def __init__(
        self,
        cmdb_urls: URLs,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        self.flavors = FlavorCRUD(
            get_url=cmdb_urls.flavors,
            post_url=cmdb_urls.providers,
            patch_url=cmdb_urls.flavors,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.identity_providers = IdentityProviderCRUD(
            get_url=cmdb_urls.identity_providers,
            post_url=cmdb_urls.identity_providers,
            patch_url=cmdb_urls.identity_providers,
            connect_url=cmdb_urls.providers,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.images = ImageCRUD(
            get_url=cmdb_urls.images,
            post_url=cmdb_urls.providers,
            patch_url=cmdb_urls.images,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.locations = LocationCRUD(
            get_url=cmdb_urls.locations,
            post_url=cmdb_urls.locations,
            patch_url=cmdb_urls.locations,
            connect_url=cmdb_urls.providers,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.projects = ProjectCRUD(
            get_url=cmdb_urls.projects,
            post_url=cmdb_urls.providers,
            patch_url=cmdb_urls.projects,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.providers = ProviderCRUD(
            get_url=cmdb_urls.providers,
            post_url=cmdb_urls.providers,
            patch_url=cmdb_urls.providers,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.quotas = QuotaCRUD(
            get_url=cmdb_urls.quotas,
            post_url=cmdb_urls.quotas,
            patch_url=cmdb_urls.quotas,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.services = ServiceCRUD(
            get_url=cmdb_urls.services,
            post_url=cmdb_urls.providers,
            patch_url=cmdb_urls.services,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        # slas = None
        # user_groups = None
