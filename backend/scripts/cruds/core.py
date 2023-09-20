from typing import Any, Dict, Generic, List, Optional, Tuple, Type, TypeVar

import requests
from fastapi import status
from fastapi.encoders import jsonable_encoder
from logger import logger
from pydantic import UUID4, AnyHttpUrl, BaseModel

ReadSchema = TypeVar("ReadSchema", bound=BaseModel)
QuerySchema = TypeVar("QuerySchema", bound=BaseModel)
WriteSchema = TypeVar("WriteSchema", bound=BaseModel)


class ConnectionException(Exception):
    def __init__(self, resp: requests.Response, item_repr: str) -> None:
        msg = f"Failed to connect {item_repr}\n"
        msg += f"Status code: {resp.status_code}"
        msg += f"Message: {resp.text}"
        logger.error(msg)
        super().__init__(msg)


class CreationException(Exception):
    def __init__(self, resp: requests.Response, item_repr: str) -> None:
        msg = f"Failed to create {item_repr}\n"
        msg += f"Status code: {resp.status_code}"
        msg += f"Message: {resp.text}"
        logger.error(msg)
        super().__init__(msg)


class DisconnectionException(Exception):
    def __init__(self, resp: requests.Response, item_repr: str) -> None:
        msg = f"Failed to disconnect {item_repr}\n"
        msg += f"Status code: {resp.status_code}"
        msg += f"Message: {resp.text}"
        logger.error(msg)
        super().__init__(msg)


class UpdateException(Exception):
    def __init__(self, resp: requests.Response, item_repr: str) -> None:
        msg = f"Failed to update {item_repr}\n"
        msg += f"Status code: {resp.status_code}"
        msg += f"Message: {resp.text}"
        logger.error(msg)
        super().__init__(msg)


class FindException(Exception):
    def __init__(self, resp: requests.Response, item_repr: str) -> None:
        msg = f"Failed to search {item_repr}\n"
        msg += f"Status code: {resp.status_code}"
        msg += f"Message: {resp.text}"
        logger.error(msg)
        super().__init__(msg)


class DeleteException(Exception):
    def __init__(self, resp: requests.Response, item_repr: str) -> None:
        msg = f"Failed to delete {item_repr}\n"
        msg += f"Status code: {resp.status_code}"
        msg += f"Message: {resp.text}"
        logger.error(msg)
        super().__init__(msg)


class DatabaseCorruptedException(Exception):
    def __init__(self, item_repr: str) -> None:
        msg = f"Multiple occurrences found for {item_repr} when one expected.\n"
        msg += "Database may be corrupted."
        logger.error(msg)
        super().__init__(msg)


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

    def create(
        self,
        *,
        new_data: WriteSchema,
        params: Optional[Dict[str, Any]] = None,
        parent_uid: Optional[UUID4] = None,
    ) -> ReadSchema:
        """Create new instance."""
        logger.info(f"Creating new {self.type}={new_data}")
        resp = requests.post(
            url=self.post_url.format(parent_uid=str(parent_uid)),
            json=jsonable_encoder(new_data),
            headers=self.write_headers,
            params=params,
        )
        if resp.status_code == status.HTTP_201_CREATED:
            logger.info(f"{self.type}={new_data} successfully created")
            return self.read_schema(**resp.json())
        raise CreationException(resp=resp, item_repr=f"{self.type}={new_data}")

    def update(self, *, new_data: WriteSchema, uid: UUID4) -> Optional[ReadSchema]:
        """Update existing instance."""
        logger.info(f"Trying to update {self.type}={new_data}.")
        resp = requests.patch(
            url=self.patch_url.format(uid=str(uid)),
            json=jsonable_encoder(new_data),
            headers=self.write_headers,
        )
        if resp.status_code == status.HTTP_200_OK:
            logger.info(f"{self.type}={new_data} successfully updated")
            return self.read_schema(**resp.json())
        if resp.status_code == status.HTTP_304_NOT_MODIFIED:
            logger.info(
                f"New data match stored data. {self.type}={new_data} not modified"
            )
            return None
        raise UpdateException(resp=resp, item_repr=f"{self.type}={new_data}")

    def single(
        self, *, data: Optional[QuerySchema] = None, with_conn: bool = False
    ) -> Optional[ReadSchema]:
        """Find single instance with given params."""
        resp = requests.get(
            url=self.get_url,
            params={**data.dict(exclude_unset=True), "with_conn": with_conn},
            headers=self.read_headers,
        )
        if resp.status_code == status.HTTP_200_OK:
            if len(resp.json()) == 0:
                logger.info(f"{self.type}={data} not found")
                return None
            if len(resp.json()) == 1:
                logger.info(f"{self.type}={data} found")
                return self.read_schema(**resp.json()[0])
            raise DatabaseCorruptedException(item_repr=f"{self.type}={data}")
        raise FindException(resp=resp, item_repr=f"{self.type}={data}")

    def find_in_list(
        self, *, data: QuerySchema, db_items: List[ReadSchema], exact: bool = True
    ) -> Tuple[Optional[ReadSchema], int]:
        """Find instance within a given list with corresponding key-value
        pair."""
        d = data.dict(exclude_unset=True)
        for idx, db_item in enumerate(db_items):
            i = db_item.dict()
            if not exact:
                for k, v in d.items():
                    if i.get(k) == v:
                        logger.info(
                            f"{self.type}={data} already belongs to this provider"
                        )
                        return (db_item, idx)
            else:
                if all([i.get(k) == v for k, v in d.items()]):
                    logger.info(f"{self.type}={data} already belongs to this provider")
                    return (db_item, idx)
        logger.info(f"No {self.type}={data} belongs to this provider.")
        return (None, -1)

    def remove(self, *, uid: UUID4) -> None:
        """Remove item."""
        resp = requests.delete(
            url=self.patch_url.format(uid=uid), headers=self.write_headers
        )
        if resp.status_code == status.HTTP_204_NO_CONTENT:
            return None
        raise DeleteException(resp=resp, item_repr=f"{self.type}={uid}")

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
        updated_item = self.update(new_data=item, uid=db_item.uid)
        return db_item if updated_item is None else updated_item


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

    def connect(
        self, *, uid: UUID4, parent_uid: UUID4, conn_data: Optional[Any] = None
    ) -> None:
        """Connect item to another entity."""
        logger.info(f"Connecting {self.type}.")
        resp = requests.put(
            url=self.connect_url.format(parent_uid=parent_uid, uid=uid),
            headers=self.write_headers,
            json=jsonable_encoder(conn_data),
        )
        if resp.status_code == status.HTTP_200_OK:
            logger.info("Successfully connected")
        elif resp.status_code == status.HTTP_304_NOT_MODIFIED:
            logger.info("Already connected. Data not modified")
        else:
            raise ConnectionException(resp=resp, item_repr=f"{self.type}={str(uid)}")

    def disconnect(self, *, uid: UUID4, parent_uid: UUID4) -> None:
        """Disconnect item from another entity."""
        logger.info(f"Disconnecting {self.type}.")
        resp = requests.delete(
            url=self.connect_url.format(parent_uid=parent_uid, uid=uid),
            headers=self.write_headers,
        )
        if resp.status_code == status.HTTP_200_OK:
            logger.info("Successfully disconnected")
        elif resp.status_code == status.HTTP_304_NOT_MODIFIED:
            logger.info("Already disconnected. Data not modified")
        else:
            raise DisconnectionException(resp=resp, item_repr=f"{self.type}={str(uid)}")
