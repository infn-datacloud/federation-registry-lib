import os
from typing import Any, Dict, List, Optional

import requests
from app.provider.schemas_extended import ProviderCreateExtended as ProviderWrite
from app.provider.schemas_extended import ProviderReadExtended as ProviderRead
from fastapi import status
from fastapi.encoders import jsonable_encoder
from logger import logger
from pydantic import UUID4, AnyHttpUrl

TIMEOUT = 5  # s


class CRUD:
    def __init__(
        self,
        *,
        url: AnyHttpUrl,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        self.type = "Provider"
        self.read_headers = read_headers
        self.write_headers = write_headers
        self.list_url = url
        self.item_url = os.path.join(url, "{uid}")

    def read(self, *, with_conn: bool = False) -> List[ProviderRead]:
        """Retrieve all instances of this type."""
        logger.info(f"Looking for all {self.type}s")

        resp = requests.get(
            url=self.list_url,
            params={"with_conn": with_conn},
            headers=self.read_headers,
            timeout=TIMEOUT,
        )
        if resp.status_code == status.HTTP_200_OK:
            return [ProviderRead(**i) for i in resp.json()]

        logger.error("GET operation failed")
        logger.error(f"Status code: {resp.status_code}")
        logger.error(f"Message: {resp.text}")
        raise Exception("GET operation failed")

    def create(
        self,
        *,
        data: ProviderWrite,
        params: Optional[Dict[str, Any]] = None,
    ) -> ProviderRead:
        """Create new instance."""
        logger.info(f"Creating new {self.type}={data.name}")
        logger.debug("New Data:")
        logger.debug(f"{data}")

        resp = requests.post(
            url=self.list_url,
            json=jsonable_encoder(data),
            headers=self.write_headers,
            params=params,
            timeout=TIMEOUT,
        )
        if resp.status_code == status.HTTP_201_CREATED:
            logger.info("Created")
            return ProviderRead(**resp.json())

        logger.error(f"Failed to create {self.type}={data.name}")
        logger.error(f"Status code: {resp.status_code}")
        logger.error(f"Message: {resp.text}")
        raise Exception(f"Failed to create {self.type}={data.name}")

    def remove(self, *, item: ProviderRead) -> None:
        """Remove item."""
        logger.info(f"Removing {self.type}={item.name}.")

        resp = requests.delete(
            url=self.item_url.format(uid=item.uid),
            headers=self.write_headers,
            timeout=TIMEOUT,
        )
        if resp.status_code == status.HTTP_204_NO_CONTENT:
            logger.info("Removed")
            return None

        logger.error(f"Failed to remove {self.type}={item.name}")
        logger.error(f"Status code: {resp.status_code}")
        logger.error(f"Message: {resp.text}")
        raise Exception(f"Failed to remove {self.type}={item.name}")

    def update(self, *, new_data: ProviderWrite, uid: UUID4) -> Optional[ProviderRead]:
        """Update existing instance."""
        logger.info(f"Trying to update {self.type}={new_data.name}.")

        resp = requests.put(
            url=self.item_url.format(uid=str(uid)),
            json=jsonable_encoder(new_data),
            headers=self.write_headers,
            timeout=TIMEOUT,
        )
        if resp.status_code == status.HTTP_200_OK:
            logger.info(f"{self.type}={new_data} successfully updated")
            return ProviderRead(**resp.json())

        if resp.status_code == status.HTTP_304_NOT_MODIFIED:
            logger.info(
                f"New data match stored data. {self.type}={new_data.name} not modified"
            )
            return None

        logger.error(f"Failed to update {self.type}={new_data.name}")
        logger.error(f"Status code: {resp.status_code}")
        logger.error(f"Message: {resp.text}")
        raise Exception(f"Failed to update {self.type}={new_data.name}")
