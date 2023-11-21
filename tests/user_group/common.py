import json
from typing import Any, Dict, Generic, Optional, Type, TypeVar

from fastapi import status
from fastapi.testclient import TestClient
from neomodel import UniqueIdProperty
from pydantic import BaseModel

from app.config import get_settings
from app.models import BaseNodeRead

API_PARAMS_SINGLE_ITEM = [None, {"short": True}, {"with_conn": True}]
API_PARAMS_MULTIPLE_ITEMS = [None, {"short": True}, {"with_conn": True}]


UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)


class BaseAPI(Generic[UpdateSchemaType]):
    def __init__(self, *, endpoint_group: str) -> None:
        settings = get_settings()
        self.api_v1 = settings.API_V1_STR
        self.endpoint_group = endpoint_group

    def read(
        self,
        *,
        client: TestClient,
        target_uid: UniqueIdProperty,
        target_status_code: int = status.HTTP_200_OK,
        params: Optional[Dict[str, str]] = None,
    ) -> Any:
        """Execute a GET operation to read an item from its UID.

        Assert response is 200 and return jsonified data."""
        response = client.get(
            f"{self.api_v1}/{self.endpoint_group}/{target_uid}", params=params
        )
        assert response.status_code == target_status_code
        return response.json()

    def read_multi(
        self, *, client: TestClient, target_status_code: int = status.HTTP_200_OK
    ) -> Any:
        """Execute a GET operation to read an item from its UID.

        Assert response is 200 and return jsonified data."""
        response = client.get(f"{self.api_v1}/{self.endpoint_group}/")
        assert response.status_code == target_status_code
        return response.json()

    def patch(
        self,
        *,
        client: TestClient,
        uid: UniqueIdProperty,
        new_data: UpdateSchemaType,
        target_status_code: int = status.HTTP_200_OK,
    ) -> Any:
        """Execute a PATCH operation to update a specific item.

        Retrieve the item using its UID and send, as json data, the new data.
        """
        response = client.patch(
            f"{self.api_v1}/{self.endpoint_group}/{uid}",
            json=json.loads(new_data.json()),
        )
        assert response.status_code == target_status_code
        return response.json()

    def delete(
        self,
        *,
        client: TestClient,
        uid: UniqueIdProperty,
        target_status_code: int = status.HTTP_204_NO_CONTENT,
    ) -> None:
        """Execute a DELETE operation to delete a specific item.

        Delete the item using its UID."""
        response = client.delete(f"{self.api_v1}/{self.endpoint_group}/{uid}")
        assert response.status_code == target_status_code


class BaseAPITests(BaseAPI, Generic[UpdateSchemaType, ReadSchemaType]):
    def __init__(
        self, *, endpoint_group: str, read_schema: Type[ReadSchemaType]
    ) -> None:
        super().__init__(endpoint_group=endpoint_group)
        self.read_schema = read_schema

    def test_read_item(self, *, client: TestClient, item: BaseNodeRead) -> None:
        """Execute GET operations to read all user_groups."""
        obj = self.read(client=client, target_uid=item.uid)
        return obj
