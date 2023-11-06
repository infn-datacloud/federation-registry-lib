import json
from typing import Dict
from uuid import uuid4

from app.config import get_settings
from app.quota.models import BlockStorageQuota
from app.quota.schemas import (
    BlockStorageQuotaBase,
    BlockStorageQuotaRead,
    BlockStorageQuotaReadShort,
)
from app.quota.schemas_extended import BlockStorageQuotaReadExtended
from fastapi import status
from fastapi.testclient import TestClient
from tests.utils.block_storage_quota import (
    create_random_block_storage_quota_patch,
    validate_read_block_storage_quota_attrs,
    validate_read_extended_block_storage_quota_attrs,
    validate_read_short_block_storage_quota_attrs,
)


def test_read_block_storage_quotas(
    db_block_storage_quota: BlockStorageQuota,
    db_block_storage_quota_per_user: BlockStorageQuota,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all block_storage_quotas."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/block_storage_quotas/", headers=read_header
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_block_storage_quota.uid:
        resp_bsq = content[0]
        resp_bsq_per_user = content[1]
    else:
        resp_bsq = content[1]
        resp_bsq_per_user = content[0]

    validate_read_block_storage_quota_attrs(
        obj_out=BlockStorageQuotaRead(**resp_bsq), db_item=db_block_storage_quota
    )
    validate_read_block_storage_quota_attrs(
        obj_out=BlockStorageQuotaRead(**resp_bsq_per_user),
        db_item=db_block_storage_quota_per_user,
    )


def test_read_block_storage_quotas_with_target_params(
    db_block_storage_quota: BlockStorageQuota,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all block_storage_quotas matching specific
    attributes passed as query attributes."""
    settings = get_settings()

    for k in BlockStorageQuotaBase.__fields__.keys():
        response = client.get(
            f"{settings.API_V1_STR}/block_storage_quotas/",
            params={k: db_block_storage_quota.__getattribute__(k)},
            headers=read_header,
        )
        assert response.status_code == status.HTTP_200_OK
        content = response.json()
        assert len(content) == 1
        validate_read_block_storage_quota_attrs(
            obj_out=BlockStorageQuotaRead(**content[0]), db_item=db_block_storage_quota
        )


def test_read_block_storage_quotas_with_limit(
    db_block_storage_quota: BlockStorageQuota,
    db_block_storage_quota_per_user: BlockStorageQuota,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all block_storage_quotas limiting the number of
    output items."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/block_storage_quotas/",
        params={"limit": 0},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = client.get(
        f"{settings.API_V1_STR}/block_storage_quotas/",
        params={"limit": 1},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1


def test_read_sorted_block_storage_quotas(
    db_block_storage_quota: BlockStorageQuota,
    db_block_storage_quota_per_user: BlockStorageQuota,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all sorted block_storage_quotas."""
    settings = get_settings()
    sorted_items = list(
        sorted(
            [db_block_storage_quota, db_block_storage_quota_per_user],
            key=lambda x: x.uid,
        )
    )

    response = client.get(
        f"{settings.API_V1_STR}/block_storage_quotas/",
        params={"sort": "uid"},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = client.get(
        f"{settings.API_V1_STR}/block_storage_quotas/",
        params={"sort": "-uid"},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid

    response = client.get(
        f"{settings.API_V1_STR}/block_storage_quotas/",
        params={"sort": "uid_asc"},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = client.get(
        f"{settings.API_V1_STR}/block_storage_quotas/",
        params={"sort": "uid_desc"},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid


def test_read_block_storage_quotas_with_skip(
    db_block_storage_quota: BlockStorageQuota,
    db_block_storage_quota_per_user: BlockStorageQuota,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all block_storage_quotas, skipping the first N
    entries."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/block_storage_quotas/",
        params={"skip": 0},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    response = client.get(
        f"{settings.API_V1_STR}/block_storage_quotas/",
        params={"skip": 1},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1

    response = client.get(
        f"{settings.API_V1_STR}/block_storage_quotas/",
        params={"skip": 2},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = client.get(
        f"{settings.API_V1_STR}/block_storage_quotas/",
        params={"skip": 3},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_block_storage_quotas_with_pagination(
    db_block_storage_quota: BlockStorageQuota,
    db_block_storage_quota_per_user: BlockStorageQuota,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all block_storage_quotas.

    Paginate returned list.
    """
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/block_storage_quotas/",
        params={"size": 1},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    if content[0]["uid"] == db_block_storage_quota.uid:
        next_page_uid = db_block_storage_quota_per_user.uid
    else:
        next_page_uid = db_block_storage_quota.uid

    response = client.get(
        f"{settings.API_V1_STR}/block_storage_quotas/",
        params={"size": 1, "page": 1},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    assert content[0]["uid"] == next_page_uid

    # Page greater than 0 but size equals None, does nothing
    response = client.get(
        f"{settings.API_V1_STR}/block_storage_quotas/",
        params={"page": 1},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    # Page index greater than maximum number of pages. Return nothing
    response = client.get(
        f"{settings.API_V1_STR}/block_storage_quotas/",
        params={"size": 1, "page": 2},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_block_storage_quotas_with_conn(
    db_block_storage_quota: BlockStorageQuota,
    db_block_storage_quota_per_user: BlockStorageQuota,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all block_storage_quotas with their
    relationships."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/block_storage_quotas/",
        params={"with_conn": True},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_block_storage_quota.uid:
        resp_bsq = content[0]
        resp_bsq_per_user = content[1]
    else:
        resp_bsq = content[1]
        resp_bsq_per_user = content[0]

    validate_read_extended_block_storage_quota_attrs(
        obj_out=BlockStorageQuotaReadExtended(**resp_bsq),
        db_item=db_block_storage_quota,
    )
    validate_read_extended_block_storage_quota_attrs(
        obj_out=BlockStorageQuotaReadExtended(**resp_bsq_per_user),
        db_item=db_block_storage_quota_per_user,
    )


def test_read_block_storage_quotas_short(
    db_block_storage_quota: BlockStorageQuota,
    db_block_storage_quota_per_user: BlockStorageQuota,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all block_storage_quotas with their shrunk
    version."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/block_storage_quotas/",
        params={"short": True},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_block_storage_quota.uid:
        resp_bsq = content[0]
        resp_bsq_per_user = content[1]
    else:
        resp_bsq = content[1]
        resp_bsq_per_user = content[0]

    validate_read_short_block_storage_quota_attrs(
        obj_out=BlockStorageQuotaReadShort(**resp_bsq), db_item=db_block_storage_quota
    )
    validate_read_short_block_storage_quota_attrs(
        obj_out=BlockStorageQuotaReadShort(**resp_bsq_per_user),
        db_item=db_block_storage_quota_per_user,
    )


def test_read_block_storage_quota(
    db_block_storage_quota: BlockStorageQuota,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read a block_storage_quota."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/block_storage_quotas/{db_block_storage_quota.uid}",
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_block_storage_quota_attrs(
        obj_out=BlockStorageQuotaRead(**content), db_item=db_block_storage_quota
    )


def test_read_block_storage_quota_with_conn(
    db_block_storage_quota: BlockStorageQuota,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read a block_storage_quota with its relationships."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/block_storage_quotas/{db_block_storage_quota.uid}",
        params={"with_conn": True},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_extended_block_storage_quota_attrs(
        obj_out=BlockStorageQuotaReadExtended(**content), db_item=db_block_storage_quota
    )


def test_read_block_storage_quota_short(
    db_block_storage_quota: BlockStorageQuota,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read the shrunk version of a block_storage_quota."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/block_storage_quotas/{db_block_storage_quota.uid}",
        params={"short": True},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_short_block_storage_quota_attrs(
        obj_out=BlockStorageQuotaReadShort(**content), db_item=db_block_storage_quota
    )


def test_read_not_existing_block_storage_quota(
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to try to read a not existing block_storage_quota."""
    settings = get_settings()
    item_uuid = uuid4()
    response = client.get(
        f"{settings.API_V1_STR}/block_storage_quotas/{item_uuid}", headers=read_header
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Block Storage Quota '{item_uuid}' not found"


def test_patch_block_storage_quota(
    db_block_storage_quota: BlockStorageQuota,
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute PATCH operations to update a block_storage_quota."""
    settings = get_settings()
    data = create_random_block_storage_quota_patch()
    data.per_user = db_block_storage_quota.per_user

    response = client.patch(
        f"{settings.API_V1_STR}/block_storage_quotas/{db_block_storage_quota.uid}",
        json=json.loads(data.json()),
        headers=write_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    for k, v in data.dict().items():
        assert content[k] == v


def test_patch_block_storage_quota_no_edit(
    db_block_storage_quota: BlockStorageQuota,
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute PATCH operations to update a block_storage_quota.

    Nothing changes.
    """
    settings = get_settings()
    data = create_random_block_storage_quota_patch(default=True)

    response = client.patch(
        f"{settings.API_V1_STR}/block_storage_quotas/{db_block_storage_quota.uid}",
        json=json.loads(data.json(exclude_unset=True)),
        headers=write_header,
    )
    assert response.status_code == status.HTTP_304_NOT_MODIFIED


def test_patch_not_existing_block_storage_quota(
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute PATCH operations to try to update a not existing block_storage_quota."""
    settings = get_settings()
    item_uuid = uuid4()
    data = create_random_block_storage_quota_patch()

    response = client.patch(
        f"{settings.API_V1_STR}/block_storage_quotas/{item_uuid}",
        json=json.loads(data.json()),
        headers=write_header,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Block Storage Quota '{item_uuid}' not found"


def test_patch_block_storage_quota_changing_per_user(
    db_block_storage_quota: BlockStorageQuota,
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute PATCH operations to try to change the per_user property of a
    block_storage_quota.

    Currently a per user block storage quota does not exist on the same project.
    """
    settings = get_settings()
    data = create_random_block_storage_quota_patch()
    data.per_user = not db_block_storage_quota.per_user

    uid = db_block_storage_quota.uid
    response = client.patch(
        f"{settings.API_V1_STR}/block_storage_quotas/{uid}",
        json=json.loads(data.json()),
        headers=write_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    for k, v in data.dict().items():
        assert content[k] == v


def test_patch_block_storage_quota_with_duplicated_per_user(
    db_block_storage_quota_per_user: BlockStorageQuota,
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute PATCH operations to try to change the per_user property of a
    block_storage_quota.

    Currently a per user block storage quota already exist s on the same project.
    """
    settings = get_settings()
    data = create_random_block_storage_quota_patch()
    data.per_user = not db_block_storage_quota_per_user.per_user

    uid = db_block_storage_quota_per_user.uid
    response = client.patch(
        f"{settings.API_V1_STR}/block_storage_quotas/{uid}",
        json=json.loads(data.json()),
        headers=write_header,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    content = response.json()
    db_project = db_block_storage_quota_per_user.project.single()
    assert (
        content["detail"] == f"Project '{db_project.uid}' "
        "already has a Block Storage Quota to not apply to each user"
    )


# TODO Add tests raising 422


def test_delete_block_storage_quota(
    db_block_storage_quota: BlockStorageQuota,
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute DELETE to remove a block_storage_quota."""
    settings = get_settings()
    response = client.delete(
        f"{settings.API_V1_STR}/block_storage_quotas/{db_block_storage_quota.uid}",
        headers=write_header,
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_not_existing_block_storage_quota(
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute DELETE operations to try to delete a not existing block_storage_quota."""
    settings = get_settings()
    item_uuid = uuid4()
    response = client.delete(
        f"{settings.API_V1_STR}/block_storage_quotas/{item_uuid}", headers=write_header
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Block Storage Quota '{item_uuid}' not found"
