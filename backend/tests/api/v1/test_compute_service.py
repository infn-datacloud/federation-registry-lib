import json
from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient

from app.config import get_settings
from app.service.enum import ServiceType
from app.service.models import ComputeService
from app.service.schemas import (
    ComputeServiceBase,
    ComputeServiceRead,
    ComputeServiceReadShort,
)
from app.service.schemas_extended import ComputeServiceReadExtended
from tests.utils.compute_service import (
    create_random_compute_service_patch,
    validate_read_compute_service_attrs,
    validate_read_extended_compute_service_attrs,
    validate_read_short_compute_service_attrs,
)


def test_read_compute_services(
    db_compute_serv: ComputeService,
    db_compute_serv2: ComputeService,
    api_client_read_only: TestClient,
) -> None:
    """Execute GET operations to read all compute_services."""
    settings = get_settings()

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/compute_services/",
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_compute_serv.uid:
        resp_id_serv = content[0]
        resp_id_serv2 = content[1]
    else:
        resp_id_serv = content[1]
        resp_id_serv2 = content[0]

    validate_read_compute_service_attrs(
        obj_out=ComputeServiceRead(**resp_id_serv), db_item=db_compute_serv
    )
    validate_read_compute_service_attrs(
        obj_out=ComputeServiceRead(**resp_id_serv2), db_item=db_compute_serv2
    )


def test_read_compute_services_with_target_params(
    db_compute_serv: ComputeService, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read all compute_services matching specific attributes
    passed as query attributes.
    """
    settings = get_settings()

    for k in ComputeServiceBase.__fields__.keys():
        response = api_client_read_only.get(
            f"{settings.API_V1_STR}/compute_services/",
            params={k: db_compute_serv.__getattribute__(k)},
        )
        assert response.status_code == status.HTTP_200_OK
        content = response.json()
        assert len(content) == 1
        validate_read_compute_service_attrs(
            obj_out=ComputeServiceRead(**content[0]), db_item=db_compute_serv
        )


def test_read_compute_services_with_limit(
    db_compute_serv: ComputeService,
    db_compute_serv2: ComputeService,
    api_client_read_only: TestClient,
) -> None:
    """Execute GET operations to read all compute_services limiting the number of output
    items.
    """
    settings = get_settings()

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/compute_services/", params={"limit": 0}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/compute_services/", params={"limit": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1


def test_read_sorted_compute_services(
    db_compute_serv: ComputeService,
    db_compute_serv2: ComputeService,
    api_client_read_only: TestClient,
) -> None:
    """Execute GET operations to read all sorted compute_services."""
    settings = get_settings()
    sorted_items = sorted([db_compute_serv, db_compute_serv2], key=lambda x: x.uid)

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/compute_services/", params={"sort": "uid"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/compute_services/", params={"sort": "-uid"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/compute_services/", params={"sort": "uid_asc"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/compute_services/", params={"sort": "uid_desc"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid


def test_read_compute_services_with_skip(
    db_compute_serv: ComputeService,
    db_compute_serv2: ComputeService,
    api_client_read_only: TestClient,
) -> None:
    """Execute GET operations to read all compute_services, skipping the first N
    entries.
    """
    settings = get_settings()

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/compute_services/", params={"skip": 0}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/compute_services/", params={"skip": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/compute_services/", params={"skip": 2}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/compute_services/", params={"skip": 3}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_compute_services_with_pagination(
    db_compute_serv: ComputeService,
    db_compute_serv2: ComputeService,
    api_client_read_only: TestClient,
) -> None:
    """Execute GET operations to read all compute_services.

    Paginate returned list.
    """
    settings = get_settings()

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/compute_services/", params={"size": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    if content[0]["uid"] == db_compute_serv.uid:
        next_page_uid = db_compute_serv2.uid
    else:
        next_page_uid = db_compute_serv.uid

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/compute_services/", params={"size": 1, "page": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    assert content[0]["uid"] == next_page_uid

    # Page greater than 0 but size equals None, does nothing
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/compute_services/", params={"page": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    # Page index greater than maximum number of pages. Return nothing
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/compute_services/", params={"size": 1, "page": 2}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_compute_services_with_conn(
    db_compute_serv: ComputeService,
    db_compute_serv2: ComputeService,
    api_client_read_only: TestClient,
) -> None:
    """Execute GET operations to read all compute_services with their relationships."""
    settings = get_settings()

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/compute_services/", params={"with_conn": True}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_compute_serv.uid:
        resp_id_serv = content[0]
        resp_id_serv2 = content[1]
    else:
        resp_id_serv = content[1]
        resp_id_serv2 = content[0]

    validate_read_extended_compute_service_attrs(
        obj_out=ComputeServiceReadExtended(**resp_id_serv),
        db_item=db_compute_serv,
    )
    validate_read_extended_compute_service_attrs(
        obj_out=ComputeServiceReadExtended(**resp_id_serv2),
        db_item=db_compute_serv2,
    )


def test_read_compute_services_short(
    db_compute_serv: ComputeService,
    db_compute_serv2: ComputeService,
    api_client_read_only: TestClient,
) -> None:
    """Execute GET operations to read all compute_services with their shrunk version."""
    settings = get_settings()

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/compute_services/", params={"short": True}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_compute_serv.uid:
        resp_id_serv = content[0]
        resp_id_serv2 = content[1]
    else:
        resp_id_serv = content[1]
        resp_id_serv2 = content[0]

    validate_read_short_compute_service_attrs(
        obj_out=ComputeServiceReadShort(**resp_id_serv),
        db_item=db_compute_serv,
    )
    validate_read_short_compute_service_attrs(
        obj_out=ComputeServiceReadShort(**resp_id_serv2),
        db_item=db_compute_serv2,
    )


def test_read_compute_service(
    db_compute_serv: ComputeService, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read a compute_service."""
    settings = get_settings()
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/compute_services/{db_compute_serv.uid}"
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_compute_service_attrs(
        obj_out=ComputeServiceRead(**content), db_item=db_compute_serv
    )


def test_read_compute_service_with_conn(
    db_compute_serv: ComputeService, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read a compute_service with its relationships."""
    settings = get_settings()
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/compute_services/{db_compute_serv.uid}",
        params={"with_conn": True},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_extended_compute_service_attrs(
        obj_out=ComputeServiceReadExtended(**content), db_item=db_compute_serv
    )


def test_read_compute_service_short(
    db_compute_serv: ComputeService, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read the shrunk version of a compute_service."""
    settings = get_settings()
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/compute_services/{db_compute_serv.uid}",
        params={"short": True},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_short_compute_service_attrs(
        obj_out=ComputeServiceReadShort(**content), db_item=db_compute_serv
    )


def test_read_not_existing_compute_service(api_client_read_only: TestClient) -> None:
    """Execute GET operations to try to read a not existing compute_service."""
    settings = get_settings()
    item_uuid = uuid4()
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/compute_services/{item_uuid}"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Compute Service '{item_uuid}' not found"


def test_patch_compute_service(
    db_compute_serv: ComputeService, api_client_read_write: TestClient
) -> None:
    """Execute PATCH operations to update a compute_service."""
    settings = get_settings()
    data = create_random_compute_service_patch()

    response = api_client_read_write.patch(
        f"{settings.API_V1_STR}/compute_services/{db_compute_serv.uid}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    for k, v in data.dict().items():
        assert content[k] == v


def test_patch_compute_service_no_edit(
    db_compute_serv: ComputeService, api_client_read_write: TestClient
) -> None:
    """Execute PATCH operations to update a compute_service.

    Nothing changes.
    """
    settings = get_settings()
    data = create_random_compute_service_patch(default=True)

    response = api_client_read_write.patch(
        f"{settings.API_V1_STR}/compute_services/{db_compute_serv.uid}",
        json=json.loads(data.json(exclude_unset=True)),
    )
    assert response.status_code == status.HTTP_304_NOT_MODIFIED


def test_patch_not_existing_compute_service(api_client_read_write: TestClient) -> None:
    """Execute PATCH operations to try to update a not existing compute_service."""
    settings = get_settings()
    item_uuid = uuid4()
    data = create_random_compute_service_patch()

    response = api_client_read_write.patch(
        f"{settings.API_V1_STR}/compute_services/{item_uuid}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Compute Service '{item_uuid}' not found"


def test_patch_compute_service_changing_type(
    db_compute_serv: ComputeService, api_client_read_write: TestClient
) -> None:
    """Execute PATCH operations to try to change the type of a compute_service.

    At first this should not be allowed by schema construction. In any case, if a
    request arrives, it is discarded since the payload is not an compute service object.
    """
    settings = get_settings()
    data = create_random_compute_service_patch()

    for t in [i.value for i in ServiceType]:
        if t != ServiceType.COMPUTE.value:
            d = json.loads(data.json())
            d["type"] = t

            response = api_client_read_write.patch(
                f"{settings.API_V1_STR}/compute_services/{db_compute_serv.uid}",
                json=d,
            )
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
            content = response.json()
            assert "Not valid type" in str(content["detail"])


def test_patch_compute_service_with_duplicated_endpoint(
    db_compute_serv: ComputeService,
    db_compute_serv2: ComputeService,
    api_client_read_write: TestClient,
) -> None:
    """Execute PATCH operations to try to assign an already existing endpoint to a
    compute_service.
    """
    settings = get_settings()
    data = create_random_compute_service_patch()
    data.endpoint = db_compute_serv.endpoint

    response = api_client_read_write.patch(
        f"{settings.API_V1_STR}/compute_services/{db_compute_serv2.uid}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    content = response.json()
    assert (
        content["detail"]
        == f"Compute Service with endpoint '{data.endpoint}' already registered"
    )


# TODO Add tests raising 422


def test_delete_compute_service(
    db_compute_serv: ComputeService, api_client_read_write: TestClient
) -> None:
    """Execute DELETE to remove a public compute_service."""
    settings = get_settings()
    response = api_client_read_write.delete(
        f"{settings.API_V1_STR}/compute_services/{db_compute_serv.uid}",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_not_existing_compute_service(api_client_read_write: TestClient) -> None:
    """Execute DELETE operations to try to delete a not existing compute_service."""
    settings = get_settings()
    item_uuid = uuid4()
    response = api_client_read_write.delete(
        f"{settings.API_V1_STR}/compute_services/{item_uuid}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Compute Service '{item_uuid}' not found"
