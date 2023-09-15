from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

import requests
from fastapi import status
from fastapi.encoders import jsonable_encoder
from logger import logger
from pydantic import UUID4, AnyHttpUrl, BaseModel

ReadSchema = TypeVar("ReadSchema", bound=BaseModel)
QuerySchema = TypeVar("QuerySchema", bound=BaseModel)
WriteSchema = TypeVar("WriteSchema", bound=BaseModel)


class BasicCRUD(Generic[WriteSchema, ReadSchema, QuerySchema]):
    def __init__(
        self,
        *,
        write_schema: Type[WriteSchema],
        read_schema: Type[ReadSchema],
        get_url: AnyHttpUrl,
        post_url: AnyHttpUrl,
        patch_url: AnyHttpUrl,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        self.type = self.__class__.__name__.replace("CRUD", "")
        self.write_schema = write_schema
        self.read_schema = read_schema
        self.get_url = get_url
        self.post_url = post_url
        self.patch_url = patch_url
        self.read_headers = read_headers
        self.write_headers = write_headers

    def _action_failed(
        self, *, resp: requests.Response, action: str, item: WriteSchema
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
        url = self.post_url.format(parent_uid=str(parent_uid))
        resp = requests.post(
            url=url,
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
        url = self.patch_url.format(uid=str(old_data.uid))
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
        d = data.dict(exclude_unset=True)
        for db_item in db_items:
            for k, v in d.items():
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
        url = self.connect_url.format(parent_uid=parent_uid, uid=uid)
        resp = requests.put(
            url=url, headers=self.write_headers, json=jsonable_encoder(data)
        )
        if resp.status_code == status.HTTP_200_OK:
            logger.info(f"{new_data} successfully connected")
        elif resp.status_code == status.HTTP_304_NOT_MODIFIED:
            logger.info(f"{new_data} already connected. Data not modified")
        else:
            self._action_failed(resp=resp, action="connect", item=new_data)
