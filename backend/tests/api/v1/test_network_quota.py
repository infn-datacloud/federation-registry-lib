import json
from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient

from app.config import get_settings
from app.quota.models import NetworkQuota
from app.quota.schemas import (
    NetworkQuotaBase,
    NetworkQuotaRead,
    NetworkQuotaReadShort,
)
from app.quota.schemas_extended import NetworkQuotaReadExtended
from tests.utils.network_quota import (
    create_random_network_quota_patch,
    validate_read_extended_network_quota_attrs,
    validate_read_network_quota_attrs,
    validate_read_short_network_quota_attrs,
)


def test_read_network_quotas(
    db_network_quota: NetworkQuota,
    db_network_quota_per_user: NetworkQuota,
    api_client_read_only: TestClient,
) -> None:
    """Execute GET operations to read all network_quotas."""
    settings = get_settings()

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/network_quotas/",
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_network_quota.uid:
        resp_bsq = content[0]
        resp_bsq_per_user = content[1]
    else:
        resp_bsq = content[1]
        resp_bsq_per_user = content[0]

    validate_read_network_quota_attrs(
        obj_out=NetworkQuotaRead(**resp_bsq), db_item=db_network_quota
    )
    validate_read_network_quota_attrs(
        obj_out=NetworkQuotaRead(**resp_bsq_per_user),
        db_item=db_network_quota_per_user,
    )


def test_read_network_quotas_with_target_params(
    db_network_quota: NetworkQuota, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read all network_quotas matching specific attributes
    passed as query attributes.
    """
    settings = get_settings()

    for k in NetworkQuotaBase.__fields__.keys():
        response = api_client_read_only.get(
            f"{settings.API_V1_STR}/network_quotas/",
            params={k: db_network_quota.__getattribute__(k)},
        )
        assert response.status_code == status.HTTP_200_OK
        content = response.json()
        assert len(content) == 1
        validate_read_network_quota_attrs(
            obj_out=NetworkQuotaRead(**content[0]), db_item=db_network_quota
        )


def test_read_network_quotas_with_limit(
    db_network_quota: NetworkQuota,
    db_network_quota_per_user: NetworkQuota,
    api_client_read_only: TestClient,
) -> None:
    """Execute GET operations to read all network_quotas limiting the number of output
    items.
    """
    settings = get_settings()

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/network_quotas/", params={"limit": 0}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/network_quotas/", params={"limit": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1


def test_read_sorted_network_quotas(
    db_network_quota: NetworkQuota,
    db_network_quota_per_user: NetworkQuota,
    api_client_read_only: TestClient,
) -> None:
    """Execute GET operations to read all sorted network_quotas."""
    settings = get_settings()
    sorted_items = sorted(
        [db_network_quota, db_network_quota_per_user],
        key=lambda x: x.uid,
    )

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/network_quotas/", params={"sort": "uid"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/network_quotas/", params={"sort": "-uid"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/network_quotas/", params={"sort": "uid_asc"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/network_quotas/", params={"sort": "uid_desc"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid


def test_read_network_quotas_with_skip(
    db_network_quota: NetworkQuota,
    db_network_quota_per_user: NetworkQuota,
    api_client_read_only: TestClient,
) -> None:
    """Execute GET operations to read all network_quotas, skipping the first N
    entries.
    """
    settings = get_settings()

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/network_quotas/", params={"skip": 0}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/network_quotas/", params={"skip": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/network_quotas/", params={"skip": 2}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/network_quotas/", params={"skip": 3}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_network_quotas_with_pagination(
    db_network_quota: NetworkQuota,
    db_network_quota_per_user: NetworkQuota,
    api_client_read_only: TestClient,
) -> None:
    """Execute GET operations to read all network_quotas.

    Paginate returned list.
    """
    settings = get_settings()

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/network_quotas/", params={"size": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    if content[0]["uid"] == db_network_quota.uid:
        next_page_uid = db_network_quota_per_user.uid
    else:
        next_page_uid = db_network_quota.uid

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/network_quotas/", params={"size": 1, "page": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    assert content[0]["uid"] == next_page_uid

    # Page greater than 0 but size equals None, does nothing
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/network_quotas/", params={"page": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    # Page index greater than maximum number of pages. Return nothing
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/network_quotas/", params={"size": 1, "page": 2}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_network_quotas_with_conn(
    db_network_quota: NetworkQuota,
    db_network_quota_per_user: NetworkQuota,
    api_client_read_only: TestClient,
) -> None:
    """Execute GET operations to read all network_quotas with their relationships."""
    settings = get_settings()

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/network_quotas/", params={"with_conn": True}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_network_quota.uid:
        resp_bsq = content[0]
        resp_bsq_per_user = content[1]
    else:
        resp_bsq = content[1]
        resp_bsq_per_user = content[0]

    validate_read_extended_network_quota_attrs(
        obj_out=NetworkQuotaReadExtended(**resp_bsq),
        db_item=db_network_quota,
    )
    validate_read_extended_network_quota_attrs(
        obj_out=NetworkQuotaReadExtended(**resp_bsq_per_user),
        db_item=db_network_quota_per_user,
    )


def test_read_network_quotas_short(
    db_network_quota: NetworkQuota,
    db_network_quota_per_user: NetworkQuota,
    api_client_read_only: TestClient,
) -> None:
    """Execute GET operations to read all network_quotas with their shrunk version."""
    settings = get_settings()

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/network_quotas/", params={"short": True}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_network_quota.uid:
        resp_bsq = content[0]
        resp_bsq_per_user = content[1]
    else:
        resp_bsq = content[1]
        resp_bsq_per_user = content[0]

    validate_read_short_network_quota_attrs(
        obj_out=NetworkQuotaReadShort(**resp_bsq), db_item=db_network_quota
    )
    validate_read_short_network_quota_attrs(
        obj_out=NetworkQuotaReadShort(**resp_bsq_per_user),
        db_item=db_network_quota_per_user,
    )


def test_read_network_quota(
    db_network_quota: NetworkQuota, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read a network_quota."""
    settings = get_settings()
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/network_quotas/{db_network_quota.uid}"
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_network_quota_attrs(
        obj_out=NetworkQuotaRead(**content), db_item=db_network_quota
    )


def test_read_network_quota_with_conn(
    db_network_quota: NetworkQuota, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read a network_quota with its relationships."""
    settings = get_settings()
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/network_quotas/{db_network_quota.uid}",
        params={"with_conn": True},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_extended_network_quota_attrs(
        obj_out=NetworkQuotaReadExtended(**content), db_item=db_network_quota
    )


def test_read_network_quota_short(
    db_network_quota: NetworkQuota, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read the shrunk version of a network_quota."""
    settings = get_settings()
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/network_quotas/{db_network_quota.uid}",
        params={"short": True},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_short_network_quota_attrs(
        obj_out=NetworkQuotaReadShort(**content), db_item=db_network_quota
    )


def test_read_not_existing_network_quota(api_client_read_only: TestClient) -> None:
    """Execute GET operations to try to read a not existing network_quota."""
    settings = get_settings()
    item_uuid = uuid4()
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/network_quotas/{item_uuid}"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Network Quota '{item_uuid}' not found"


def test_patch_network_quota(
    db_network_quota: NetworkQuota, api_client_read_write: TestClient
) -> None:
    """Execute PATCH operations to update a network_quota."""
    settings = get_settings()
    data = create_random_network_quota_patch()
    data.per_user = db_network_quota.per_user

    response = api_client_read_write.patch(
        f"{settings.API_V1_STR}/network_quotas/{db_network_quota.uid}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    for k, v in data.dict().items():
        assert content[k] == v


def test_patch_network_quota_no_edit(
    db_network_quota: NetworkQuota, api_client_read_write: TestClient
) -> None:
    """Execute PATCH operations to update a network_quota.

    Nothing changes.
    """
    settings = get_settings()
    data = create_random_network_quota_patch(default=True)

    response = api_client_read_write.patch(
        f"{settings.API_V1_STR}/network_quotas/{db_network_quota.uid}",
        json=json.loads(data.json(exclude_unset=True)),
    )
    assert response.status_code == status.HTTP_304_NOT_MODIFIED


def test_patch_not_existing_network_quota(api_client_read_write: TestClient) -> None:
    """Execute PATCH operations to try to update a not existing network_quota."""
    settings = get_settings()
    item_uuid = uuid4()
    data = create_random_network_quota_patch()

    response = api_client_read_write.patch(
        f"{settings.API_V1_STR}/network_quotas/{item_uuid}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Network Quota '{item_uuid}' not found"


def test_patch_network_quota_changing_per_user(
    db_network_quota: NetworkQuota, api_client_read_write: TestClient
) -> None:
    """Execute PATCH operations to try to change the per_user property of a
    block_storage_quota.

    Currently a per user block storage quota does not exist on the same project.
    """
    settings = get_settings()
    data = create_random_network_quota_patch()
    data.per_user = not db_network_quota.per_user

    response = api_client_read_write.patch(
        f"{settings.API_V1_STR}/network_quotas/{db_network_quota.uid}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    for k, v in data.dict().items():
        assert content[k] == v


def test_patch_network_quota_with_duplicated_per_user(
    db_network_quota_per_user: NetworkQuota, api_client_read_write: TestClient
) -> None:
    """Execute PATCH operations to try to change the per_user property of a
    block_storage_quota.

    Currently a per user block storage quota already exists on the same project.
    """
    settings = get_settings()
    data = create_random_network_quota_patch()
    data.per_user = not db_network_quota_per_user.per_user

    response = api_client_read_write.patch(
        f"{settings.API_V1_STR}/network_quotas/{db_network_quota_per_user.uid}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    content = response.json()
    db_project = db_network_quota_per_user.project.single()
    assert (
        content["detail"] == f"Project '{db_project.uid}' "
        "already has a Network Quota to not apply to each user"
    )


# TODO Add tests raising 422


def test_delete_network_quota(
    db_network_quota: NetworkQuota, api_client_read_write: TestClient
) -> None:
    """Execute DELETE to remove a network_quota."""
    settings = get_settings()
    response = api_client_read_write.delete(
        f"{settings.API_V1_STR}/network_quotas/{db_network_quota.uid}",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_not_existing_network_quota(api_client_read_write: TestClient) -> None:
    """Execute DELETE operations to try to delete a not existing network_quota."""
    settings = get_settings()
    item_uuid = uuid4()
    response = api_client_read_write.delete(
        f"{settings.API_V1_STR}/network_quotas/{item_uuid}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Network Quota '{item_uuid}' not found"
