import json
from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient

from app.config import get_settings
from app.network.models import Network
from app.network.schemas import NetworkBase, NetworkRead, NetworkReadShort
from app.network.schemas_extended import NetworkReadExtended
from tests.utils.network import (
    create_random_network_patch,
    validate_read_extended_network_attrs,
    validate_read_network_attrs,
    validate_read_short_network_attrs,
)


def test_read_networks(
    db_public_network: Network,
    db_private_network: Network,
    api_client_read_only: TestClient,
) -> None:
    """Execute GET operations to read all networks."""
    settings = get_settings()

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/networks/",
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_public_network.uid:
        resp_public_network = content[0]
        resp_private_network = content[1]
    else:
        resp_public_network = content[1]
        resp_private_network = content[0]

    validate_read_network_attrs(
        obj_out=NetworkRead(**resp_public_network), db_item=db_public_network
    )
    validate_read_network_attrs(
        obj_out=NetworkRead(**resp_private_network), db_item=db_private_network
    )


def test_read_networks_with_target_params(
    db_public_network: Network, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read all networks matching specific attributes passed
    as query attributes.
    """
    settings = get_settings()

    for k in NetworkBase.__fields__.keys():
        response = api_client_read_only.get(
            f"{settings.API_V1_STR}/networks/",
            params={k: db_public_network.__getattribute__(k)},
        )
        assert response.status_code == status.HTTP_200_OK
        content = response.json()
        assert len(content) == 1
        validate_read_network_attrs(
            obj_out=NetworkRead(**content[0]), db_item=db_public_network
        )


def test_read_networks_with_limit(
    db_public_network: Network,
    db_private_network: Network,
    api_client_read_only: TestClient,
) -> None:
    """Execute GET operations to read all networks limiting the number of output
    items.
    """
    settings = get_settings()

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/networks/", params={"limit": 0}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/networks/", params={"limit": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1


def test_read_sorted_networks(
    db_public_network: Network,
    db_private_network: Network,
    api_client_read_only: TestClient,
) -> None:
    """Execute GET operations to read all sorted networks."""
    settings = get_settings()
    sorted_items = sorted([db_public_network, db_private_network], key=lambda x: x.uid)

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/networks/", params={"sort": "uid"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/networks/", params={"sort": "-uid"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/networks/", params={"sort": "uid_asc"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/networks/", params={"sort": "uid_desc"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid


def test_read_networks_with_skip(
    db_public_network: Network,
    db_private_network: Network,
    api_client_read_only: TestClient,
) -> None:
    """Execute GET operations to read all networks, skipping the first N entries."""
    settings = get_settings()

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/networks/", params={"skip": 0}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/networks/", params={"skip": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/networks/", params={"skip": 2}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/networks/", params={"skip": 3}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_networks_with_pagination(
    db_public_network: Network,
    db_private_network: Network,
    api_client_read_only: TestClient,
) -> None:
    """Execute GET operations to read all networks.

    Paginate returned list.
    """
    settings = get_settings()

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/networks/", params={"size": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    if content[0]["uid"] == db_public_network.uid:
        next_page_uid = db_private_network.uid
    else:
        next_page_uid = db_public_network.uid

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/networks/", params={"size": 1, "page": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    assert content[0]["uid"] == next_page_uid

    # Page greater than 0 but size equals None, does nothing
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/networks/", params={"page": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    # Page index greater than maximum number of pages. Return nothing
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/networks/", params={"size": 1, "page": 2}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_networks_with_conn(
    db_public_network: Network,
    db_private_network: Network,
    api_client_read_only: TestClient,
) -> None:
    """Execute GET operations to read all networks with their relationships."""
    settings = get_settings()

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/networks/", params={"with_conn": True}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_public_network.uid:
        resp_public_network = content[0]
        resp_private_network = content[1]
    else:
        resp_public_network = content[1]
        resp_private_network = content[0]

    validate_read_extended_network_attrs(
        obj_out=NetworkReadExtended(**resp_public_network),
        db_item=db_public_network,
    )
    validate_read_extended_network_attrs(
        obj_out=NetworkReadExtended(**resp_private_network),
        db_item=db_private_network,
    )


def test_read_networks_short(
    db_public_network: Network,
    db_private_network: Network,
    api_client_read_only: TestClient,
) -> None:
    """Execute GET operations to read all networks with their shrunk version."""
    settings = get_settings()

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/networks/", params={"short": True}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_public_network.uid:
        resp_public_network = content[0]
        resp_private_network = content[1]
    else:
        resp_public_network = content[1]
        resp_private_network = content[0]

    validate_read_short_network_attrs(
        obj_out=NetworkReadShort(**resp_public_network),
        db_item=db_public_network,
    )
    validate_read_short_network_attrs(
        obj_out=NetworkReadShort(**resp_private_network),
        db_item=db_private_network,
    )


def test_read_network(
    db_public_network: Network, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read a network."""
    settings = get_settings()
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/networks/{db_public_network.uid}"
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_network_attrs(
        obj_out=NetworkRead(**content), db_item=db_public_network
    )


def test_read_public_network_with_conn(
    db_public_network: Network, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read a public network with its relationships."""
    settings = get_settings()
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/networks/{db_public_network.uid}",
        params={"with_conn": True},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_extended_network_attrs(
        obj_out=NetworkReadExtended(**content), db_item=db_public_network
    )


def test_read_private_network_with_conn(
    db_private_network: Network, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read a private network with its relationships."""
    settings = get_settings()
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/networks/{db_private_network.uid}",
        params={"with_conn": True},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_extended_network_attrs(
        obj_out=NetworkReadExtended(**content), db_item=db_private_network
    )


def test_read_network_short(
    db_public_network: Network, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read the shrunk version of a network."""
    settings = get_settings()
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/networks/{db_public_network.uid}",
        params={"short": True},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_short_network_attrs(
        obj_out=NetworkReadShort(**content), db_item=db_public_network
    )


def test_read_not_existing_network(api_client_read_only: TestClient) -> None:
    """Execute GET operations to try to read a not existing network."""
    settings = get_settings()
    item_uuid = uuid4()
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/networks/{item_uuid}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Network '{item_uuid}' not found"


def test_patch_public_network(
    db_public_network: Network, api_client_read_write: TestClient
) -> None:
    """Execute PATCH operations to update a public network."""
    settings = get_settings()
    data = create_random_network_patch()
    data.is_shared = db_public_network.is_shared

    response = api_client_read_write.patch(
        f"{settings.API_V1_STR}/networks/{db_public_network.uid}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    for k, v in data.dict().items():
        assert content[k] == v


def test_patch_private_network(
    db_private_network: Network, api_client_read_write: TestClient
) -> None:
    """Execute PATCH operations to update a private network."""
    settings = get_settings()
    data = create_random_network_patch()
    data.is_shared = db_private_network.is_shared

    response = api_client_read_write.patch(
        f"{settings.API_V1_STR}/networks/{db_private_network.uid}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    for k, v in data.dict().items():
        assert content[k] == v


def test_patch_network_no_edit(
    db_public_network: Network, api_client_read_write: TestClient
) -> None:
    """Execute PATCH operations to update a network.

    Nothing changes.
    """
    settings = get_settings()
    data = create_random_network_patch(default=True)

    response = api_client_read_write.patch(
        f"{settings.API_V1_STR}/networks/{db_public_network.uid}",
        json=json.loads(data.json(exclude_unset=True)),
    )
    assert response.status_code == status.HTTP_304_NOT_MODIFIED


def test_patch_not_existing_network(api_client_read_write: TestClient) -> None:
    """Execute PATCH operations to try to update a not existing network."""
    settings = get_settings()
    item_uuid = uuid4()
    data = create_random_network_patch()

    response = api_client_read_write.patch(
        f"{settings.API_V1_STR}/networks/{item_uuid}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Network '{item_uuid}' not found"


def test_patch_network_changing_visibility(
    db_private_network: Network, api_client_read_write: TestClient
) -> None:
    """Execute PATCH operations to try to change the visibility of a network."""
    settings = get_settings()
    data = create_random_network_patch()
    data.is_shared = not db_private_network.is_shared

    response = api_client_read_write.patch(
        f"{settings.API_V1_STR}/networks/{db_private_network.uid}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    content = response.json()
    assert content["detail"] == "Network visibility can't be changed"


def test_patch_network_with_duplicated_uuid(
    db_public_network: Network,
    db_private_network: Network,
    api_client_read_write: TestClient,
) -> None:
    """Execute PATCH operations to try to assign an already existing UUID to a
    network.
    """
    settings = get_settings()
    data = create_random_network_patch()
    data.is_shared = db_private_network.is_shared
    data.uuid = db_public_network.uuid

    response = api_client_read_write.patch(
        f"{settings.API_V1_STR}/networks/{db_private_network.uid}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    content = response.json()
    assert content["detail"] == f"Network with uuid '{data.uuid}' already registered"


# TODO Add tests raising 422


def test_delete_public_network(
    db_public_network: Network, api_client_read_write: TestClient
) -> None:
    """Execute DELETE to remove a public network."""
    settings = get_settings()
    response = api_client_read_write.delete(
        f"{settings.API_V1_STR}/networks/{db_public_network.uid}",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_private_network(
    db_private_network: Network, api_client_read_write: TestClient
) -> None:
    """Execute DELETE to remove a private network."""
    settings = get_settings()
    response = api_client_read_write.delete(
        f"{settings.API_V1_STR}/networks/{db_private_network.uid}",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_not_existing_network(api_client_read_write: TestClient) -> None:
    """Execute DELETE operations to try to delete a not existing network."""
    settings = get_settings()
    item_uuid = uuid4()
    response = api_client_read_write.delete(
        f"{settings.API_V1_STR}/networks/{item_uuid}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Network '{item_uuid}' not found"
