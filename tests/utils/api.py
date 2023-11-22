import json
from typing import Dict, List, Optional, Type
from uuid import uuid4

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response

from app.config import get_settings
from tests.fixtures.client import (
    CLIENTS,
    CLIENTS_FAILING_AUTHN,
    CLIENTS_NO_TOKEN,
    CLIENTS_READ_ONLY,
    CLIENTS_READ_WRITE,
)
from tests.utils.schemas import (
    BasicPublicSchemaType,
    BasicSchemaType,
    ModelType,
    SchemaValidation,
    UpdateSchemaType,
)

API_PARAMS_SINGLE_ITEM = [{}, {"short": True}, {"with_conn": True}]
API_PARAMS_MULTIPLE_ITEMS = [
    {},
    {"sort": "uid"},
    {"sort": "-uid"},
    {"sort": "uid_asc"},
    {"sort": "uid_desc"},
    {"sort": "uid", "limit": 0},
    {"sort": "uid", "limit": 1},
    {"sort": "uid", "limit": 2},
    {"sort": "uid", "skip": 0},
    {"sort": "uid", "skip": 1},
    {"sort": "uid", "skip": 2},
    {"sort": "uid", "size": 1},
    {"sort": "uid", "size": 1, "page": 1},
    {"sort": "uid", "page": 1},
    {"sort": "uid", "size": 1, "page": 2},
    {"short": True},
    {"with_conn": True},
]


class BaseAPI(
    SchemaValidation[
        ModelType, BasicSchemaType, BasicPublicSchemaType, UpdateSchemaType
    ]
):
    def __init__(
        self,
        *,
        base_schema: Type[BasicSchemaType],
        base_public_schema: Type[BasicPublicSchemaType],
        endpoint_group: str,
        item_name: str,
    ) -> None:
        super().__init__(base_schema=base_schema, base_public_schema=base_public_schema)
        settings = get_settings()
        self.api_v1 = settings.API_V1_STR
        self.endpoint_group = endpoint_group
        self.item_name = item_name

    def read(
        self,
        *,
        client: TestClient,
        db_item: Optional[ModelType] = None,
        params: Optional[Dict[str, str]] = None,
        target_status_code: int = status.HTTP_200_OK,
        public: bool = False,
    ) -> Response:
        """Execute a GET operation to read an item from its UID.

        Assert response is 200 and return jsonified data."""
        target_uid = db_item.uid if db_item else uuid4()
        response = client.get(
            f"{self.api_v1}/{self.endpoint_group}/{target_uid}", params=params
        )
        if not db_item:
            target_status_code = status.HTTP_404_NOT_FOUND

        assert response.status_code == target_status_code
        if target_status_code == status.HTTP_200_OK:
            extended = params.get("with_conn") is not None
            self._validate_read_attrs(
                obj=response.json(), db_item=db_item, public=public, extended=extended
            )
        elif target_status_code == status.HTTP_404_NOT_FOUND:
            assert (
                response.json()["detail"]
                == f"{self.item_name} '{target_uid}' not found"
            )

        return response

    def read_multi(
        self,
        *,
        client: TestClient,
        db_items: Optional[List[ModelType]] = None,
        params: Optional[Dict[str, str]] = None,
        target_status_code: int = status.HTTP_200_OK,
        public: bool = False,
    ) -> Response:
        """Execute a GET operation to read an item from its UID.

        Assert response is 200 and return jsonified data."""
        if not db_items:
            db_items = []

        response = client.get(f"{self.api_v1}/{self.endpoint_group}/", params=params)
        assert response.status_code == target_status_code

        extended = params.get("with_conn") is not None

        db_sorted_items = list(sorted(db_items, key=lambda x: x.uid))
        sorted_items = response.json()
        if not params.get("sort"):
            sorted_items = sorted(sorted_items, key=lambda x: x.get("uid"))
        elif params.get("sort").startswith("-") or params.get("sort").endswith("_desc"):
            db_sorted_items.reverse()

        if params.get("limit") is not None:
            db_sorted_items = db_sorted_items[: params.get("limit")]
        if params.get("skip") is not None:
            db_sorted_items = db_sorted_items[params.get("skip") :]
        page = params.get("page", 0)
        if params.get("size") is not None:
            start = page * params.get("size")
            end = start + params.get("size")
            db_sorted_items = db_sorted_items[start:end]
        assert len(response.json()) == len(db_sorted_items)

        for obj, db_item in zip(sorted_items, db_sorted_items):
            assert obj.get("uid") == db_item.uid
            self._validate_read_attrs(
                obj=obj, db_item=db_item, public=public, extended=extended
            )

        return response

    def patch(
        self,
        *,
        client: TestClient,
        new_data: UpdateSchemaType,
        db_item: Optional[ModelType] = None,
        target_status_code: int = status.HTTP_200_OK,
    ) -> Response:
        """Execute a PATCH operation to update a specific item.

        Retrieve the item using its UID and send, as json data, the new data.
        """
        target_uid = db_item.uid if db_item else uuid4()
        response = client.patch(
            f"{self.api_v1}/{self.endpoint_group}/{target_uid}",
            json=json.loads(new_data.json(exclude_unset=True)),
        )
        if not db_item:
            target_status_code = status.HTTP_404_NOT_FOUND

        assert response.status_code == target_status_code
        if target_status_code == status.HTTP_200_OK:
            self._validate_read_attrs(obj=response.json(), db_item=db_item)
        elif target_status_code == status.HTTP_304_NOT_MODIFIED:
            pass
        elif target_status_code == status.HTTP_401_UNAUTHORIZED:
            assert response.json()["error"] == "Unauthenticated"
            # TODO assert the item is still there
        elif target_status_code == status.HTTP_403_FORBIDDEN:
            assert response.json()["detail"] == "Not authenticated"
            # TODO assert the item is still there
        elif target_status_code == status.HTTP_404_NOT_FOUND:
            assert (
                response.json()["detail"]
                == f"{self.item_name} '{target_uid}' not found"
            )

        return response

    def delete(
        self,
        *,
        client: TestClient,
        db_item: Optional[ModelType] = None,
        target_status_code: int = status.HTTP_204_NO_CONTENT,
    ) -> Response:
        """Execute a DELETE operation to delete a specific item.

        Delete the item using its UID."""
        target_uid = db_item.uid if db_item else uuid4()
        response = client.delete(f"{self.api_v1}/{self.endpoint_group}/{target_uid}")
        if not db_item:
            target_status_code = status.HTTP_404_NOT_FOUND

        assert response.status_code == target_status_code
        if target_status_code == status.HTTP_401_UNAUTHORIZED:
            assert response.json()["error"] == "Unauthenticated"
            # TODO assert the item is still there
        elif target_status_code == status.HTTP_403_FORBIDDEN:
            assert response.json()["detail"] == "Not authenticated"
            # TODO assert the item is still there
        elif target_status_code == status.HTTP_404_NOT_FOUND:
            assert (
                response.json()["detail"]
                == f"{self.item_name} '{target_uid}' not found"
            )
            # TODO assert the item does not exists.

        return response


class TestBaseAPI:
    __test__ = False
    api: str
    db_item1: str
    db_item2: str
    db_item3: str

    @pytest.mark.parametrize("client, public", CLIENTS)
    @pytest.mark.parametrize("params", API_PARAMS_SINGLE_ITEM)
    def test_read_item(
        self,
        request: pytest.FixtureRequest,
        client: TestClient,
        public: bool,
        params: Optional[Dict[str, str]],
    ) -> None:
        """Execute GET operations to read a specific item.

        Execute this operation using both authenticated and not-authenticated clients.
        For each, repeat the operation passing 'short', 'with_conn' and no params.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        api.read(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item1),
            params=params,
            public=public,
        )

    @pytest.mark.parametrize("client, public", CLIENTS)
    def test_read_not_existing_item(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute GET operations to try to read a not existing item.

        Execute this operation using both authenticated and not-authenticated clients.
        The endpoint returns a 404 error.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        api.read(client=request.getfixturevalue(client))

    @pytest.mark.parametrize("client, public", CLIENTS)
    @pytest.mark.parametrize("params", API_PARAMS_MULTIPLE_ITEMS)
    def test_read_items(
        self,
        request: pytest.FixtureRequest,
        client: TestClient,
        public: bool,
        params: Optional[Dict[str, str]],
    ) -> None:
        """Execute GET operations to read all items.

        Execute this operation using both authenticated and not-authenticated clients.
        For each, repeat the operation passing 'sort', 'limit', 'skip', 'size', 'page',
        'short', 'with_conn' and no params. When using params limiting the size of the
        returned list use also sort to have a predictable response.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        api.read_multi(
            client=request.getfixturevalue(client),
            db_items=[
                request.getfixturevalue(self.db_item2),
                request.getfixturevalue(self.db_item3),
            ],
            params=params,
            public=public,
        )

    @pytest.mark.parametrize("client, public", CLIENTS)
    @pytest.mark.parametrize("params", API_PARAMS_MULTIPLE_ITEMS)
    def test_read_items_no_entries(
        self,
        request: pytest.FixtureRequest,
        client: TestClient,
        public: bool,
        params: Optional[Dict[str, str]],
    ) -> None:
        """Execute GET operations to read all items. But there are no items.

        Execute this operation using both authenticated and not-authenticated clients.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        api.read_multi(client=request.getfixturevalue(client), params=params)

    @pytest.mark.parametrize("client, public", CLIENTS)
    def test_read_item_with_target_params(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute GET operations to read all items matching specific attributes.

        Execute this operation using both authenticated and not-authenticated clients.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        if public:
            keys = api.base_public_schema.__fields__.keys()
        else:
            keys = api.base_schema.__fields__.keys()

        db_item = request.getfixturevalue(self.db_item2)
        for k in keys:
            api.read_multi(
                client=request.getfixturevalue(client),
                db_items=[db_item],
                params={k: db_item.__getattribute__(k)},
                public=public,
            )

    @pytest.mark.parametrize("client, public", CLIENTS_NO_TOKEN)
    def test_patch_item_no_authn(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to update a specific item.

        Client not authenticated. The endpoints raises a 403 error.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        new_data = api.random_patch_item()
        api.patch(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item1),
            target_status_code=status.HTTP_403_FORBIDDEN,
            new_data=new_data,
        )

    @pytest.mark.parametrize(
        "client, public", CLIENTS_FAILING_AUTHN + CLIENTS_READ_ONLY
    )
    def test_patch_item_no_authz(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to update a specific item.

        Client with no write access. The endpoints raises a 401 error.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        new_data = api.random_patch_item()
        api.patch(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item1),
            target_status_code=status.HTTP_401_UNAUTHORIZED,
            new_data=new_data,
        )

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_item_authz(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to update a specific item.

        Update the item attributes in the database.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        new_data = api.random_patch_item()
        api.patch(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item1),
            new_data=new_data,
        )

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_item_empty_obj(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to update a specific item.

        New item is an empty object (none values has been discarded).
        No changes. The endpoint returns a 304 message.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        new_data = api.random_patch_item(default=True)
        api.patch(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item1),
            target_status_code=status.HTTP_304_NOT_MODIFIED,
            new_data=new_data,
        )

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_item_no_edit(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to update a specific item.

        New item attributes are the same as the existing one.
        No changes. The endpoint returns a 304 message.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item = request.getfixturevalue(self.db_item1)
        new_data = api.random_patch_item(from_item=db_item)
        api.patch(
            client=request.getfixturevalue(client),
            db_item=db_item,
            target_status_code=status.HTTP_304_NOT_MODIFIED,
            new_data=new_data,
        )

    @pytest.mark.parametrize("client, public", CLIENTS)
    def test_patch_not_existing_item(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a not existing item.

        Execute this operation using both authenticated and not-authenticated clients.
        The endpoint returns a 404 error.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        new_data = api.random_patch_item()
        api.patch(client=request.getfixturevalue(client), new_data=new_data)

    @pytest.mark.parametrize("client, public", CLIENTS_NO_TOKEN)
    def test_delete_item_no_authn(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute DELETE operations to delete a specific item.

        Client not authenticated. The endpoints raises a 403 error.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        api.delete(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item1),
            target_status_code=status.HTTP_403_FORBIDDEN,
        )

    @pytest.mark.parametrize(
        "client, public", CLIENTS_FAILING_AUTHN + CLIENTS_READ_ONLY
    )
    def test_delete_item_no_authz(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute DELETE operations to delete a specific item.

        Client with no write access. The endpoints raises a 401 error.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        api.delete(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item1),
            target_status_code=status.HTTP_401_UNAUTHORIZED,
        )

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_delete_item_authz(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute DELETE operations to delete a specific item.

        Delete the item from the database.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        api.delete(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item1),
        )

    @pytest.mark.parametrize("client, public", CLIENTS)
    def test_delete_not_existing_item(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute DELETE operations to try to delete a not existing item.

        Execute this operation using both authenticated and not-authenticated clients.
        The endpoint returns a 404 error.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        api.delete(client=request.getfixturevalue(client))
