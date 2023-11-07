import json
from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient

from app.config import get_settings
from app.sla.models import SLA
from app.sla.schemas import SLABase, SLAReadPublic
from app.sla.schemas_extended import SLAReadExtendedPublic
from tests.utils.sla import (
    create_random_sla_patch,
    validate_read_extended_public_sla_attrs,
    validate_read_public_sla_attrs,
)


def test_read_slas(
    db_sla2: SLA,
    db_sla3: SLA,
    client: TestClient,
) -> None:
    """Execute GET operations to read all slas."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/slas/",
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_sla2.uid:
        resp_sla = content[0]
        resp_sla2 = content[1]
    else:
        resp_sla = content[1]
        resp_sla2 = content[0]

    validate_read_public_sla_attrs(obj_out=SLAReadPublic(**resp_sla), db_item=db_sla2)
    validate_read_public_sla_attrs(obj_out=SLAReadPublic(**resp_sla2), db_item=db_sla3)


def test_read_slas_with_target_params(
    db_sla: SLA,
    client: TestClient,
) -> None:
    """Execute GET operations to read all slas matching specific attributes passed as
    query attributes.
    """
    settings = get_settings()

    for k in SLABase.__fields__.keys():
        response = client.get(
            f"{settings.API_V1_STR}/slas/",
            params={k: db_sla.__getattribute__(k)},
        )
        assert response.status_code == status.HTTP_200_OK
        content = response.json()
        assert len(content) == 1
        validate_read_public_sla_attrs(
            obj_out=SLAReadPublic(**content[0]), db_item=db_sla
        )


def test_read_slas_with_limit(
    db_sla2: SLA,
    client: TestClient,
) -> None:
    """Execute GET operations to read all slas limiting the number of output items."""
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/slas/", params={"limit": 0})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = client.get(f"{settings.API_V1_STR}/slas/", params={"limit": 1})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1


def test_read_sorted_slas(
    db_sla2: SLA,
    db_sla3: SLA,
    client: TestClient,
) -> None:
    """Execute GET operations to read all sorted slas."""
    settings = get_settings()
    sorted_items = sorted([db_sla2, db_sla3], key=lambda x: x.uid)

    response = client.get(f"{settings.API_V1_STR}/slas/", params={"sort": "uid"})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = client.get(f"{settings.API_V1_STR}/slas/", params={"sort": "-uid"})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid

    response = client.get(f"{settings.API_V1_STR}/slas/", params={"sort": "uid_asc"})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = client.get(
        f"{settings.API_V1_STR}/slas/",
        params={"sort": "uid_desc"},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid


def test_read_slas_with_skip(
    db_sla2: SLA,
    client: TestClient,
) -> None:
    """Execute GET operations to read all slas, skipping the first N entries."""
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/slas/", params={"skip": 0})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    response = client.get(f"{settings.API_V1_STR}/slas/", params={"skip": 1})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1

    response = client.get(f"{settings.API_V1_STR}/slas/", params={"skip": 2})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = client.get(f"{settings.API_V1_STR}/slas/", params={"skip": 3})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_slas_with_pagination(
    db_sla2: SLA,
    db_sla3: SLA,
    client: TestClient,
) -> None:
    """Execute GET operations to read all slas.

    Paginate returned list.
    """
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/slas/", params={"size": 1})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    if content[0]["uid"] == db_sla2.uid:
        next_page_uid = db_sla3.uid
    else:
        next_page_uid = db_sla2.uid

    response = client.get(f"{settings.API_V1_STR}/slas/", params={"size": 1, "page": 1})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    assert content[0]["uid"] == next_page_uid

    # Page greater than 0 but size equals None, does nothing
    response = client.get(f"{settings.API_V1_STR}/slas/", params={"page": 1})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    # Page index greater than maximum number of pages. Return nothing
    response = client.get(f"{settings.API_V1_STR}/slas/", params={"size": 1, "page": 2})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_slas_with_conn(
    db_sla2: SLA,
    db_sla3: SLA,
    client: TestClient,
) -> None:
    """Execute GET operations to read all slas with their relationships."""
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/slas/", params={"with_conn": True})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_sla2.uid:
        resp_sla = content[0]
        resp_sla2 = content[1]
    else:
        resp_sla = content[1]
        resp_sla2 = content[0]

    validate_read_extended_public_sla_attrs(
        obj_out=SLAReadExtendedPublic(**resp_sla), db_item=db_sla2
    )
    validate_read_extended_public_sla_attrs(
        obj_out=SLAReadExtendedPublic(**resp_sla2), db_item=db_sla3
    )


def test_read_slas_short(
    db_sla2: SLA,
    db_sla3: SLA,
    client: TestClient,
) -> None:
    """Execute GET operations to read all SLAs with their shrunk version."""
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/slas/", params={"short": True})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_sla2.uid:
        resp_sla = content[0]
        resp_sla2 = content[1]
    else:
        resp_sla = content[1]
        resp_sla2 = content[0]

    # TODO
    # with pytest.raises(ValidationError):
    #     q = SLAReadShort(**resp_sla)
    # with pytest.raises(ValidationError):
    #     q = SLAReadShort(**resp_sla2)

    validate_read_public_sla_attrs(obj_out=SLAReadPublic(**resp_sla), db_item=db_sla2)
    validate_read_public_sla_attrs(obj_out=SLAReadPublic(**resp_sla2), db_item=db_sla3)


def test_read_sla(
    db_sla: SLA,
    client: TestClient,
) -> None:
    """Execute GET operations to read an SLA."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/slas/{db_sla.uid}",
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_public_sla_attrs(obj_out=SLAReadPublic(**content), db_item=db_sla)


def test_read_sla_with_conn(
    db_sla: SLA,
    client: TestClient,
) -> None:
    """Execute GET operations to read an SLA with its relationships."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/slas/{db_sla.uid}",
        params={"with_conn": True},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_extended_public_sla_attrs(
        obj_out=SLAReadExtendedPublic(**content), db_item=db_sla
    )


def test_read_sla_short(
    db_sla: SLA,
    client: TestClient,
) -> None:
    """Execute GET operations to read the shrunk version of an SLA."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/slas/{db_sla.uid}", params={"short": True}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()

    # TODO
    # with pytest.raises(ValidationError):
    #     q = SLAReadShort(**content)

    validate_read_public_sla_attrs(obj_out=SLAReadPublic(**content), db_item=db_sla)


def test_read_not_existing_sla(
    client: TestClient,
) -> None:
    """Execute GET operations to try to read a not existing SLA."""
    settings = get_settings()
    item_uuid = uuid4()
    response = client.get(
        f"{settings.API_V1_STR}/slas/{item_uuid}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"SLA '{item_uuid}' not found"


def test_patch_sla(
    db_sla: SLA,
    client: TestClient,
) -> None:
    """Execute PATCH operations to update an SLA.

    No access rights. Permission denied
    """
    settings = get_settings()
    data = create_random_sla_patch()
    response = client.patch(
        f"{settings.API_V1_STR}/slas/{db_sla.uid}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = response.json()
    assert content["detail"] == "Not authenticated"


def test_patch_not_existing_sla(
    client: TestClient,
) -> None:
    """Execute PATCH operations to update a not existing SLA.

    No access rights. Permission denied
    """
    settings = get_settings()
    data = create_random_sla_patch()
    response = client.patch(
        f"{settings.API_V1_STR}/slas/{uuid4()}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = response.json()
    assert content["detail"] == "Not authenticated"


def test_delete_sla(
    db_sla: SLA,
    client: TestClient,
) -> None:
    """Execute PATCH operations to update an SLA.

    No access rights. Permission denied
    """
    settings = get_settings()
    response = client.delete(f"{settings.API_V1_STR}/slas/{db_sla.uid}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = response.json()
    assert content["detail"] == "Not authenticated"


def test_delete_not_existing_sla(
    client: TestClient,
) -> None:
    """Execute PATCH operations to update a not existing SLA.

    No access rights. Permission denied
    """
    settings = get_settings()
    response = client.delete(f"{settings.API_V1_STR}/slas/{uuid4()}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = response.json()
    assert content["detail"] == "Not authenticated"
