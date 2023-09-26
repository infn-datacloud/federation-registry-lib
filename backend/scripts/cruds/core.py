import os
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

import requests
from fastapi import status
from fastapi.encoders import jsonable_encoder
from logger import logger
from pydantic import UUID4, AnyHttpUrl, BaseModel

ReadSchema = TypeVar("ReadSchema", bound=BaseModel)
QuerySchema = TypeVar("QuerySchema", bound=BaseModel)
WriteSchema = TypeVar("WriteSchema", bound=BaseModel)

TIMEOUT = 5  # s


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
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
        url: AnyHttpUrl,
        parent_url: Optional[AnyHttpUrl] = None,
        connectable_items: List[str] = [],
    ) -> None:
        self.type = self.__class__.__name__.replace("CRUD", "")
        self.write_schema = write_schema
        self.read_schema = read_schema
        self.read_headers = read_headers
        self.write_headers = write_headers
        self.get_multi_url = url
        self.item_url = os.path.join(url, "{uid}")
        if parent_url is None:
            self.post_url = url
        else:
            self.post_url = os.path.join(
                parent_url, "{parent_uid}", os.path.basename(os.path.normpath(url))
            )
        self.connect_urls = {}
        for item in connectable_items:
            self.connect_urls[item] = os.path.join(url, "{uid}", item, "{partner_uid}")

    def all(self, *, with_conn: bool = False) -> List[ReadSchema]:
        """Retrieve all instances of this type."""
        logger.info(f"Looking for all {self.type}")

        resp = requests.get(
            url=self.get_multi_url,
            params={"with_conn": with_conn},
            headers=self.read_headers,
            timeout=TIMEOUT,
        )
        if resp.status_code == status.HTTP_200_OK:
            return [self.read_schema(**i) for i in resp.json()]

        raise FindException(resp=resp, item_repr=f"{self.type}")

    def connect(  # TODO review attr names
        self, *, uid: UUID4, parent_uid: UUID4, conn_data: Optional[Any] = None
    ) -> None:
        """Connect item to another entity."""
        logger.info(f"Connecting {self.type}.")
        resp = requests.put(
            url=self.connect_url.format(parent_uid=parent_uid, uid=uid),
            headers=self.write_headers,
            json=jsonable_encoder(conn_data, by_alias=False),
            timeout=TIMEOUT,
        )
        if resp.status_code == status.HTTP_200_OK:
            logger.info("Successfully connected")
        elif resp.status_code == status.HTTP_304_NOT_MODIFIED:
            logger.info("Already connected. Data not modified")
        else:
            raise ConnectionException(resp=resp, item_repr=f"{self.type}={str(uid)}")

    def create(
        self,
        *,
        data: WriteSchema,
        params: Optional[Dict[str, Any]] = None,
        parent_uid: Optional[UUID4] = None,
    ) -> ReadSchema:
        """Create new instance."""
        str_item = data.dict(by_alias=True).get("_id")
        logger.info(f"Creating new {self.type}={str_item}")

        resp = requests.post(
            url=self.post_url.format(parent_uid=str(parent_uid)),
            json=jsonable_encoder(data, by_alias=False),
            headers=self.write_headers,
            params=params,
            timeout=TIMEOUT,
        )
        if resp.status_code == status.HTTP_201_CREATED:
            logger.info(f"{self.type}={str_item} successfully created")
            return self.read_schema(**resp.json())

        raise CreationException(resp=resp, item_repr=f"{self.type}={str_item}")

    def disconnect(  # TODO review attr names
        self, *, uid: UUID4, parent_uid: UUID4
    ) -> None:
        """Disconnect item from another entity."""
        logger.info(f"Disconnecting {self.type}.")
        resp = requests.delete(
            url=self.connect_url.format(parent_uid=parent_uid, uid=uid),
            headers=self.write_headers,
            timeout=TIMEOUT,
        )
        if resp.status_code == status.HTTP_200_OK:
            logger.info("Successfully disconnected")
        elif resp.status_code == status.HTTP_304_NOT_MODIFIED:
            logger.info("Already disconnected. Data not modified")
        else:
            raise DisconnectionException(resp=resp, item_repr=f"{self.type}={str(uid)}")

    def remove(self, *, item: ReadSchema) -> None:
        """Remove item."""
        str_item = item.dict(by_alias=True).get("_id")
        logger.info(f"Removing {self.type}={str_item}.")

        resp = requests.delete(
            url=self.item_url.format(uid=item.uid),
            headers=self.write_headers,
            timeout=TIMEOUT,
        )
        if resp.status_code == status.HTTP_204_NO_CONTENT:
            return None

        raise DeleteException(resp=resp, item_repr=f"{self.type}={str_item}")

    def single(
        self, *, data: Optional[QuerySchema] = None, with_conn: bool = False
    ) -> Optional[ReadSchema]:
        """Find single instance with given params."""
        str_item = data.dict(by_alias=True).get("_id")
        logger.info(f"Looking for {self.type}={str_item}")

        resp = requests.get(
            url=self.get_multi_url,
            params={**data.dict(exclude_unset=True), "with_conn": with_conn},
            headers=self.read_headers,
            timeout=TIMEOUT,
        )
        if resp.status_code == status.HTTP_200_OK:
            if len(resp.json()) == 0:
                logger.info(f"{self.type}={data} not found")
                return None
            if len(resp.json()) == 1:
                logger.info(f"{self.type}={data} found")
                return self.read_schema(**resp.json()[0])

            raise DatabaseCorruptedException(item_repr=f"{self.type}={str_item}")

        raise FindException(resp=resp, item_repr=f"{self.type}={str_item}")

    def update(self, *, new_data: WriteSchema, uid: UUID4) -> Optional[ReadSchema]:
        """Update existing instance."""
        str_item = new_data.dict(by_alias=True).get("_id")
        logger.info(f"Trying to update {self.type}={str_item}.")

        resp = requests.patch(
            url=self.item_url.format(uid=str(uid)),
            json=jsonable_encoder(new_data, by_alias=False),
            headers=self.write_headers,
            timeout=TIMEOUT,
        )
        if resp.status_code == status.HTTP_200_OK:
            logger.info(f"{self.type}={new_data} successfully updated")
            return self.read_schema(**resp.json())

        if resp.status_code == status.HTTP_304_NOT_MODIFIED:
            logger.info(
                f"New data match stored data. {self.type}={str_item} not modified"
            )
            return None

        raise UpdateException(resp=resp, item_repr=f"{self.type}={str_item}")
