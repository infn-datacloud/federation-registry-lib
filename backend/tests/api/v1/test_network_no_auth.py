import json
from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient

from app.config import get_settings
from app.network.models import Network
from app.network.schemas import NetworkBase, NetworkReadPublic
from app.network.schemas_extended import NetworkReadExtendedPublic
from tests.utils.network import (
    create_random_network_patch,
    validate_read_extended_public_network_attrs,
    validate_read_public_network_attrs,
)


def test_read_networks(
    db_public_network: Network,
    db_private_network: Network,
    client: TestClient,
) -> None:
    """Execute GET operations to read all networks."""
    settings = get_settings()

    response = client.get(
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

    validate_read_public_network_attrs(
        obj_out=NetworkReadPublic(**resp_public_network),
        db_item=db_public_network,
    )
    validate_read_public_network_attrs(
        obj_out=NetworkReadPublic(**resp_private_network),
        db_item=db_private_network,
    )


def test_read_networks_with_target_params(
    db_public_network: Network,
    client: TestClient,
) -> None:
    """Execute GET operations to read all networks matching specific attributes passed
    as query attributes.
    """
    settings = get_settings()

    for k in NetworkBase.__fields__.keys():
        response = client.get(
            f"{settings.API_V1_STR}/networks/",
            params={k: db_public_network.__getattribute__(k)},
        )
        assert response.status_code == status.HTTP_200_OK
        content = response.json()
        assert len(content) == 1
        validate_read_public_network_attrs(
            obj_out=NetworkReadPublic(**content[0]), db_item=db_public_network
        )


def test_read_networks_with_limit(
    db_public_network: Network,
    db_private_network: Network,
    client: TestClient,
) -> None:
    """Execute GET operations to read all networks limiting the number of output
    items.
    """
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/networks/", params={"limit": 0})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = client.get(f"{settings.API_V1_STR}/networks/", params={"limit": 1})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1


def test_read_sorted_networks(
    db_public_network: Network,
    db_private_network: Network,
    client: TestClient,
) -> None:
    """Execute GET operations to read all sorted networks."""
    settings = get_settings()
    sorted_items = list(
        sorted([db_public_network, db_private_network], key=lambda x: x.uid)
    )

    response = client.get(f"{settings.API_V1_STR}/networks/", params={"sort": "uid"})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = client.get(f"{settings.API_V1_STR}/networks/", params={"sort": "-uid"})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid

    response = client.get(
        f"{settings.API_V1_STR}/networks/", params={"sort": "uid_asc"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = client.get(
        f"{settings.API_V1_STR}/networks/",
        params={"sort": "uid_desc"},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid


def test_read_networks_with_skip(
    db_public_network: Network,
    db_private_network: Network,
    client: TestClient,
) -> None:
    """Execute GET operations to read all networks, skipping the first N entries."""
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/networks/", params={"skip": 0})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    response = client.get(f"{settings.API_V1_STR}/networks/", params={"skip": 1})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1

    response = client.get(f"{settings.API_V1_STR}/networks/", params={"skip": 2})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = client.get(f"{settings.API_V1_STR}/networks/", params={"skip": 3})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_networks_with_pagination(
    db_public_network: Network,
    db_private_network: Network,
    client: TestClient,
) -> None:
    """Execute GET operations to read all networks.

    Paginate returned list.
    """
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/networks/", params={"size": 1})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    if content[0]["uid"] == db_public_network.uid:
        next_page_uid = db_private_network.uid
    else:
        next_page_uid = db_public_network.uid

    response = client.get(
        f"{settings.API_V1_STR}/networks/", params={"size": 1, "page": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    assert content[0]["uid"] == next_page_uid

    # Page greater than 0 but size equals None, does nothing
    response = client.get(f"{settings.API_V1_STR}/networks/", params={"page": 1})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    # Page index greater than maximum number of pages. Return nothing
    response = client.get(
        f"{settings.API_V1_STR}/networks/", params={"size": 1, "page": 2}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_networks_with_conn(
    db_public_network: Network,
    db_private_network: Network,
    client: TestClient,
) -> None:
    """Execute GET operations to read all networks with their relationships."""
    settings = get_settings()

    response = client.get(
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

    validate_read_extended_public_network_attrs(
        obj_out=NetworkReadExtendedPublic(**resp_public_network),
        db_item=db_public_network,
    )
    validate_read_extended_public_network_attrs(
        obj_out=NetworkReadExtendedPublic(**resp_private_network),
        db_item=db_private_network,
    )


def test_read_networks_short(
    db_public_network: Network,
    db_private_network: Network,
    client: TestClient,
) -> None:
    """Execute GET operations to read all networks with their shrunk version."""
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/networks/", params={"short": True})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_public_network.uid:
        resp_public_network = content[0]
        resp_private_network = content[1]
    else:
        resp_public_network = content[1]
        resp_private_network = content[0]

    # TODO
    # with pytest.raises(ValidationError):
    #     q = NetworkReadShort(**resp_public_network)
    # with pytest.raises(ValidationError):
    #     q = NetworkReadShort(**resp_private_network)

    validate_read_public_network_attrs(
        obj_out=NetworkReadPublic(**resp_public_network),
        db_item=db_public_network,
    )
    validate_read_public_network_attrs(
        obj_out=NetworkReadPublic(**resp_private_network),
        db_item=db_private_network,
    )


def test_read_network(
    db_public_network: Network,
    client: TestClient,
) -> None:
    """Execute GET operations to read a network."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/networks/{db_public_network.uid}",
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_public_network_attrs(
        obj_out=NetworkReadPublic(**content), db_item=db_public_network
    )


def test_read_public_network_with_conn(
    db_public_network: Network,
    client: TestClient,
) -> None:
    """Execute GET operations to read a public network with its relationships."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/networks/{db_public_network.uid}",
        params={"with_conn": True},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_extended_public_network_attrs(
        obj_out=NetworkReadExtendedPublic(**content), db_item=db_public_network
    )


def test_read_private_network_with_conn(
    db_private_network: Network,
    client: TestClient,
) -> None:
    """Execute GET operations to read a private network with its relationships."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/networks/{db_private_network.uid}",
        params={"with_conn": True},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_extended_public_network_attrs(
        obj_out=NetworkReadExtendedPublic(**content),
        db_item=db_private_network,
    )


def test_read_network_short(
    db_public_network: Network,
    client: TestClient,
) -> None:
    """Execute GET operations to read the shrunk version of a network."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/networks/{db_public_network.uid}",
        params={"short": True},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()

    # TODO
    # with pytest.raises(ValidationError):
    #     q = NetworkReadShort(**content)

    validate_read_public_network_attrs(
        obj_out=NetworkReadPublic(**content), db_item=db_public_network
    )


def test_read_not_existing_network(
    client: TestClient,
) -> None:
    """Execute GET operations to try to read a not existing network."""
    settings = get_settings()
    item_uuid = uuid4()
    response = client.get(
        f"{settings.API_V1_STR}/networks/{item_uuid}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Network '{item_uuid}' not found"


def test_patch_network(
    db_public_network: Network,
    client: TestClient,
) -> None:
    """Execute PATCH operations to update a network.

    No access rights. Permission denied
    """
    settings = get_settings()
    data = create_random_network_patch()
    response = client.patch(
        f"{settings.API_V1_STR}/networks/{db_public_network.uid}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = response.json()
    assert content["detail"] == "Not authenticated"


def test_patch_not_existing_network(
    client: TestClient,
) -> None:
    """Execute PATCH operations to update a not existing network.

    No access rights. Permission denied
    """
    settings = get_settings()
    data = create_random_network_patch()
    response = client.patch(
        f"{settings.API_V1_STR}/networks/{uuid4()}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = response.json()
    assert content["detail"] == "Not authenticated"


def test_delete_network(
    db_public_network: Network,
    client: TestClient,
) -> None:
    """Execute PATCH operations to update a network.

    No access rights. Permission denied
    """
    settings = get_settings()
    response = client.delete(f"{settings.API_V1_STR}/networks/{db_public_network.uid}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = response.json()
    assert content["detail"] == "Not authenticated"


def test_delete_not_existing_network(
    client: TestClient,
) -> None:
    """Execute PATCH operations to update a not existing network.

    No access rights. Permission denied
    """
    settings = get_settings()
    response = client.delete(f"{settings.API_V1_STR}/networks/{uuid4()}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = response.json()
    assert content["detail"] == "Not authenticated"
