import json
from uuid import uuid4

from app.config import get_settings
from app.service.models import IdentityService
from app.service.schemas import IdentityServiceBase, IdentityServiceReadPublic
from app.service.schemas_extended import IdentityServiceReadExtendedPublic
from fastapi import status
from fastapi.testclient import TestClient
from tests.utils.identity_service import (
    create_random_identity_service_patch,
    validate_read_extended_public_identity_service_attrs,
    validate_read_public_identity_service_attrs,
)


def test_read_identity_services(
    db_identity_serv: IdentityService,
    db_identity_serv2: IdentityService,
    client: TestClient,
) -> None:
    """Execute GET operations to read all identity_services."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/identity_services/",
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_identity_serv.uid:
        resp_id_serv = content[0]
        resp_id_serv2 = content[1]
    else:
        resp_id_serv = content[1]
        resp_id_serv2 = content[0]

    validate_read_public_identity_service_attrs(
        obj_out=IdentityServiceReadPublic(**resp_id_serv), db_item=db_identity_serv
    )
    validate_read_public_identity_service_attrs(
        obj_out=IdentityServiceReadPublic(**resp_id_serv2), db_item=db_identity_serv2
    )


def test_read_identity_services_with_target_params(
    db_identity_serv: IdentityService,
    client: TestClient,
) -> None:
    """Execute GET operations to read all identity_services matching specific attributes
    passed as query attributes."""
    settings = get_settings()

    for k in IdentityServiceBase.__fields__.keys():
        response = client.get(
            f"{settings.API_V1_STR}/identity_services/",
            params={k: db_identity_serv.__getattribute__(k)},
        )
        assert response.status_code == status.HTTP_200_OK
        content = response.json()
        assert len(content) == 1
        validate_read_public_identity_service_attrs(
            obj_out=IdentityServiceReadPublic(**content[0]), db_item=db_identity_serv
        )


def test_read_identity_services_with_limit(
    db_identity_serv: IdentityService,
    db_identity_serv2: IdentityService,
    client: TestClient,
) -> None:
    """Execute GET operations to read all identity_services limiting the number of
    output items."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/identity_services/", params={"limit": 0}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = client.get(
        f"{settings.API_V1_STR}/identity_services/", params={"limit": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1


def test_read_sorted_identity_services(
    db_identity_serv: IdentityService,
    db_identity_serv2: IdentityService,
    client: TestClient,
) -> None:
    """Execute GET operations to read all sorted identity_services."""
    settings = get_settings()
    sorted_items = list(
        sorted([db_identity_serv, db_identity_serv2], key=lambda x: x.uid)
    )

    response = client.get(
        f"{settings.API_V1_STR}/identity_services/", params={"sort": "uid"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = client.get(
        f"{settings.API_V1_STR}/identity_services/", params={"sort": "-uid"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid

    response = client.get(
        f"{settings.API_V1_STR}/identity_services/", params={"sort": "uid_asc"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = client.get(
        f"{settings.API_V1_STR}/identity_services/",
        params={"sort": "uid_desc"},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid


def test_read_identity_services_with_skip(
    db_identity_serv: IdentityService,
    db_identity_serv2: IdentityService,
    client: TestClient,
) -> None:
    """Execute GET operations to read all identity_services, skipping the first N
    entries."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/identity_services/", params={"skip": 0}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    response = client.get(
        f"{settings.API_V1_STR}/identity_services/", params={"skip": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1

    response = client.get(
        f"{settings.API_V1_STR}/identity_services/", params={"skip": 2}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = client.get(
        f"{settings.API_V1_STR}/identity_services/", params={"skip": 3}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_identity_services_with_pagination(
    db_identity_serv: IdentityService,
    db_identity_serv2: IdentityService,
    client: TestClient,
) -> None:
    """Execute GET operations to read all identity_services.

    Paginate returned list.
    """
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/identity_services/", params={"size": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    if content[0]["uid"] == db_identity_serv.uid:
        next_page_uid = db_identity_serv2.uid
    else:
        next_page_uid = db_identity_serv.uid

    response = client.get(
        f"{settings.API_V1_STR}/identity_services/", params={"size": 1, "page": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    assert content[0]["uid"] == next_page_uid

    # Page greater than 0 but size equals None, does nothing
    response = client.get(
        f"{settings.API_V1_STR}/identity_services/", params={"page": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    # Page index greater than maximum number of pages. Return nothing
    response = client.get(
        f"{settings.API_V1_STR}/identity_services/", params={"size": 1, "page": 2}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_identity_services_with_conn(
    db_identity_serv: IdentityService,
    db_identity_serv2: IdentityService,
    client: TestClient,
) -> None:
    """Execute GET operations to read all identity_services with their relationships."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/identity_services/", params={"with_conn": True}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_identity_serv.uid:
        resp_id_serv = content[0]
        resp_id_serv2 = content[1]
    else:
        resp_id_serv = content[1]
        resp_id_serv2 = content[0]

    validate_read_extended_public_identity_service_attrs(
        obj_out=IdentityServiceReadExtendedPublic(**resp_id_serv),
        db_item=db_identity_serv,
    )
    validate_read_extended_public_identity_service_attrs(
        obj_out=IdentityServiceReadExtendedPublic(**resp_id_serv2),
        db_item=db_identity_serv2,
    )


def test_read_identity_services_short(
    db_identity_serv: IdentityService,
    db_identity_serv2: IdentityService,
    client: TestClient,
) -> None:
    """Execute GET operations to read all identity_services with their shrunk
    version."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/identity_services/", params={"short": True}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_identity_serv.uid:
        resp_id_serv = content[0]
        resp_id_serv2 = content[1]
    else:
        resp_id_serv = content[1]
        resp_id_serv2 = content[0]

    # TODO
    # with pytest.raises(ValidationError):
    #     q = IdentityServiceReadShort(**resp_id_serv)
    # with pytest.raises(ValidationError):
    #     q = IdentityServiceReadShort(**resp_id_serv2)

    validate_read_public_identity_service_attrs(
        obj_out=IdentityServiceReadPublic(**resp_id_serv), db_item=db_identity_serv
    )
    validate_read_public_identity_service_attrs(
        obj_out=IdentityServiceReadPublic(**resp_id_serv2), db_item=db_identity_serv2
    )


def test_read_identity_service(
    db_identity_serv: IdentityService,
    client: TestClient,
) -> None:
    """Execute GET operations to read a identity_service."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/identity_services/{db_identity_serv.uid}",
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_public_identity_service_attrs(
        obj_out=IdentityServiceReadPublic(**content), db_item=db_identity_serv
    )


def test_read_identity_service_with_conn(
    db_identity_serv: IdentityService,
    client: TestClient,
) -> None:
    """Execute GET operations to read a identity_service with its relationships."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/identity_services/{db_identity_serv.uid}",
        params={"with_conn": True},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_extended_public_identity_service_attrs(
        obj_out=IdentityServiceReadExtendedPublic(**content), db_item=db_identity_serv
    )


def test_read_identity_service_short(
    db_identity_serv: IdentityService,
    client: TestClient,
) -> None:
    """Execute GET operations to read the shrunk version of a identity_service."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/identity_services/{db_identity_serv.uid}",
        params={"short": True},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()

    # TODO
    # with pytest.raises(ValidationError):
    #     q = IdentityServiceReadShort(**content)

    validate_read_public_identity_service_attrs(
        obj_out=IdentityServiceReadPublic(**content), db_item=db_identity_serv
    )


def test_read_not_existing_identity_service(
    client: TestClient,
) -> None:
    """Execute GET operations to try to read a not existing identity_service."""
    settings = get_settings()
    item_uuid = uuid4()
    response = client.get(
        f"{settings.API_V1_STR}/identity_services/{item_uuid}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Identity Service '{item_uuid}' not found"


def test_patch_identity_service(
    db_identity_serv: IdentityService,
    client: TestClient,
) -> None:
    """Execute PATCH operations to update a identity_service.

    No access rights. Permission denied
    """
    settings = get_settings()
    data = create_random_identity_service_patch()
    response = client.patch(
        f"{settings.API_V1_STR}/identity_services/{db_identity_serv.uid}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = response.json()
    assert content["detail"] == "Not authenticated"


def test_patch_not_existing_identity_service(
    client: TestClient,
) -> None:
    """Execute PATCH operations to update a not existing identity_service.

    No access rights. Permission denied
    """
    settings = get_settings()
    data = create_random_identity_service_patch()
    response = client.patch(
        f"{settings.API_V1_STR}/identity_services/{uuid4()}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = response.json()
    assert content["detail"] == "Not authenticated"


def test_delete_identity_service(
    db_identity_serv: IdentityService,
    client: TestClient,
) -> None:
    """Execute PATCH operations to update a identity_service.

    No access rights. Permission denied
    """
    settings = get_settings()
    response = client.delete(
        f"{settings.API_V1_STR}/identity_services/{db_identity_serv.uid}"
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = response.json()
    assert content["detail"] == "Not authenticated"


def test_delete_not_existing_identity_service(
    client: TestClient,
) -> None:
    """Execute PATCH operations to update a not existing identity_service.

    No access rights. Permission denied
    """
    settings = get_settings()
    response = client.delete(f"{settings.API_V1_STR}/identity_services/{uuid4()}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = response.json()
    assert content["detail"] == "Not authenticated"
