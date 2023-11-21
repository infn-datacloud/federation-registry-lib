import json
from typing import Any, Dict, Generic, Optional, Type, TypeVar
from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient
from neomodel import StructuredNode
from pydantic import BaseModel

from app.config import get_settings
from app.models import BaseNode
from app.user_group.models import UserGroup
from app.user_group.schemas import UserGroupBase, UserGroupUpdate
from tests.utils.utils import random_lower_string

API_PARAMS_SINGLE_ITEM = [{}, {"short": True}, {"with_conn": True}]
API_PARAMS_MULTIPLE_ITEMS = [None, {"short": True}, {"with_conn": True}]


ModelType = TypeVar("ModelType", bound=StructuredNode)
BasicSchemaType = TypeVar("BasicSchemaType", bound=BaseNode)
BasicPublicSchemaType = TypeVar("BasicPublicSchemaType", bound=BaseNode)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class SchemaCreation:
    def __init__(self) -> None:
        super().__init__()

    def _random_patch_item(self, *, default: bool = False) -> None:
        pass


class SchemaValidation(
    SchemaCreation, Generic[ModelType, BasicSchemaType, BasicPublicSchemaType]
):
    def __init__(
        self,
        *,
        db_model: Type[ModelType],
        base_schema: Type[BasicSchemaType],
        base_public_schema: Type[BasicPublicSchemaType],
    ) -> None:
        super().__init__()
        self.db_model = db_model
        self.base_schema = base_schema
        self.base_public_schema = base_public_schema

    def _validate_attrs(
        self, *, obj: Dict[str, Any], db_item: ModelType, public: bool = False
    ) -> None:
        if public:
            attrs = self.base_public_schema.__fields__
        else:
            attrs = self.base_schema.__fields__
        for attr in attrs:
            assert db_item.__getattribute__(attr) == obj.pop(attr, None)

    def _validate_relationships(
        self, *, obj: Dict[str, Any], db_item: ModelType, public: bool = False
    ) -> None:
        pass

    def _validate_read_attrs(
        self,
        *,
        obj: Dict[str, Any],
        db_item: ModelType,
        public: bool = False,
        extended: bool = False,
    ) -> None:
        assert db_item.uid == obj.pop("uid", None)
        self._validate_attrs(obj=obj, db_item=db_item, public=public)
        if extended:
            self._validate_relationships(obj=obj, db_item=db_item, public=public)
        assert not obj


class BaseAPI(SchemaValidation):
    def __init__(
        self,
        *,
        db_model: type,
        base_schema: type,
        base_public_schema: type,
        endpoint_group: str,
        item_name: str,
    ) -> None:
        super().__init__(
            db_model=db_model,
            base_schema=base_schema,
            base_public_schema=base_public_schema,
        )
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
    ) -> None:
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
        db_item: Optional[ModelType] = None,
        target_status_code: int = status.HTTP_200_OK,
    ) -> None:
        """Execute a PATCH operation to update a specific item.

        Retrieve the item using its UID and send, as json data, the new data.
        """
        target_uid = db_item.uid if db_item else uuid4()
        new_data = self._random_patch_item()
        response = client.patch(
            f"{self.api_v1}/{self.endpoint_group}/{target_uid}",
            json=json.loads(new_data.json()),
        )
        if not db_item:
            target_status_code = status.HTTP_404_NOT_FOUND

        assert response.status_code == target_status_code
        if target_status_code == status.HTTP_200_OK:
            self._validate_read_attrs(obj=response.json(), db_item=db_item)
        elif target_status_code == status.HTTP_401_UNAUTHORIZED:
            assert response.json()["error"] == "Unauthenticated"
            # TODO assert the item is still there
        elif target_status_code == status.HTTP_403_FORBIDDEN:
            assert response.json()["detail"] == "Not authenticated"
        elif target_status_code == status.HTTP_404_NOT_FOUND:
            assert (
                response.json()["detail"]
                == f"{self.item_name} '{target_uid}' not found"
            )

    def delete(
        self,
        *,
        client: TestClient,
        db_item: Optional[ModelType] = None,
        target_status_code: int = status.HTTP_204_NO_CONTENT,
    ) -> None:
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


class UserGroupTest(BaseAPI):
    """Class with the basic API calls to User Group endpoints."""

    def __init__(self) -> None:
        super().__init__(
            db_model=UserGroup,
            base_schema=UserGroupBase,
            base_public_schema=UserGroupBase,
            endpoint_group="user_groups",
            item_name="User Group",
        )

    def _validate_relationships(
        self, *, obj: Dict[str, Any], db_item: UserGroup, public: bool = False
    ) -> None:
        db_idp = db_item.identity_provider.single()
        assert db_idp
        assert db_idp.uid == obj.pop("identity_provider").get("uid")

        slas = obj.pop("slas")
        assert len(db_item.slas) == len(slas)
        for db_sla, sla_schema in zip(
            sorted(db_item.slas, key=lambda x: x.uid),
            sorted(slas, key=lambda x: x.get("uid")),
        ):
            assert db_sla.uid == sla_schema.get("uid")

        return super()._validate_relationships(obj=obj, db_item=db_item, public=public)

    def _random_patch_item(self, *, default: bool = False) -> UserGroupUpdate:
        if default:
            return UserGroupUpdate()
        name = random_lower_string()
        description = random_lower_string()
        return UserGroupUpdate(name=name, description=description)
