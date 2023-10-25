import json
from uuid import uuid4

from app.config import get_settings
from app.image.models import Image
from app.image.schemas import ImageBase, ImageReadPublic
from app.image.schemas_extended import ImageReadExtendedPublic
from app.tests.utils.image import (
    create_random_image_patch,
    validate_read_extended_public_image_attrs,
    validate_read_public_image_attrs,
)
from fastapi import status
from fastapi.testclient import TestClient


def test_read_images(
    db_public_image: Image,
    db_private_image: Image,
    client: TestClient,
) -> None:
    """Execute GET operations to read all images."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/images/",
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_public_image.uid:
        resp_public_image = content[0]
        resp_private_image = content[1]
    else:
        resp_public_image = content[1]
        resp_private_image = content[0]

    validate_read_public_image_attrs(
        obj_out=ImageReadPublic(**resp_public_image), db_item=db_public_image
    )
    validate_read_public_image_attrs(
        obj_out=ImageReadPublic(**resp_private_image), db_item=db_private_image
    )


def test_read_images_with_target_params(
    db_public_image: Image,
    client: TestClient,
) -> None:
    """Execute GET operations to read all images matching specific attributes
    passed as query attributes."""
    settings = get_settings()

    for k in ImageBase.__fields__.keys():
        response = client.get(
            f"{settings.API_V1_STR}/images/",
            params={k: db_public_image.__getattribute__(k)},
        )
        assert response.status_code == status.HTTP_200_OK
        content = response.json()
        assert len(content) == 1
        validate_read_public_image_attrs(
            obj_out=ImageReadPublic(**content[0]), db_item=db_public_image
        )


def test_read_images_with_limit(
    db_public_image: Image,
    db_private_image: Image,
    client: TestClient,
) -> None:
    """Execute GET operations to read all images limiting the number of output
    items."""
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/images/", params={"limit": 0})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = client.get(f"{settings.API_V1_STR}/images/", params={"limit": 1})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1


def test_read_sorted_images(
    db_public_image: Image,
    db_private_image: Image,
    client: TestClient,
) -> None:
    """Execute GET operations to read all sorted images."""
    settings = get_settings()
    sorted_items = list(
        sorted([db_public_image, db_private_image], key=lambda x: x.uid)
    )

    response = client.get(f"{settings.API_V1_STR}/images/", params={"sort": "uid"})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = client.get(f"{settings.API_V1_STR}/images/", params={"sort": "-uid"})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid

    response = client.get(f"{settings.API_V1_STR}/images/", params={"sort": "uid_asc"})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = client.get(
        f"{settings.API_V1_STR}/images/",
        params={"sort": "uid_desc"},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid


def test_read_images_with_skip(
    db_public_image: Image,
    db_private_image: Image,
    client: TestClient,
) -> None:
    """Execute GET operations to read all images, skipping the first N
    entries."""
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/images/", params={"skip": 0})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    response = client.get(f"{settings.API_V1_STR}/images/", params={"skip": 1})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1

    response = client.get(f"{settings.API_V1_STR}/images/", params={"skip": 2})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = client.get(f"{settings.API_V1_STR}/images/", params={"skip": 3})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_images_with_pagination(
    db_public_image: Image,
    db_private_image: Image,
    client: TestClient,
) -> None:
    """Execute GET operations to read all images.

    Paginate returned list.
    """
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/images/", params={"size": 1})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    if content[0]["uid"] == db_public_image.uid:
        next_page_uid = db_private_image.uid
    else:
        next_page_uid = db_public_image.uid

    response = client.get(
        f"{settings.API_V1_STR}/images/", params={"size": 1, "page": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    assert content[0]["uid"] == next_page_uid

    # Page greater than 0 but size equals None, does nothing
    response = client.get(f"{settings.API_V1_STR}/images/", params={"page": 1})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    # Page index greater than maximum number of pages. Return nothing
    response = client.get(
        f"{settings.API_V1_STR}/images/", params={"size": 1, "page": 2}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_images_with_conn(
    db_public_image: Image,
    db_private_image: Image,
    client: TestClient,
) -> None:
    """Execute GET operations to read all images with their relationships."""
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/images/", params={"with_conn": True})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_public_image.uid:
        resp_public_image = content[0]
        resp_private_image = content[1]
    else:
        resp_public_image = content[1]
        resp_private_image = content[0]

    validate_read_extended_public_image_attrs(
        obj_out=ImageReadExtendedPublic(**resp_public_image), db_item=db_public_image
    )
    validate_read_extended_public_image_attrs(
        obj_out=ImageReadExtendedPublic(**resp_private_image),
        db_item=db_private_image,
    )


def test_read_images_short(
    db_public_image: Image,
    db_private_image: Image,
    client: TestClient,
) -> None:
    """Execute GET operations to read all images with their shrunk version."""
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/images/", params={"short": True})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_public_image.uid:
        resp_public_image = content[0]
        resp_private_image = content[1]
    else:
        resp_public_image = content[1]
        resp_private_image = content[0]

    # TODO
    # with pytest.raises(ValidationError):
    #     q = ImageReadShort(**resp_public_image)
    # with pytest.raises(ValidationError):
    #     q = ImageReadShort(**resp_private_image)

    validate_read_public_image_attrs(
        obj_out=ImageReadPublic(**resp_public_image), db_item=db_public_image
    )
    validate_read_public_image_attrs(
        obj_out=ImageReadPublic(**resp_private_image), db_item=db_private_image
    )


def test_read_image(
    db_public_image: Image,
    client: TestClient,
) -> None:
    """Execute GET operations to read an image."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/images/{db_public_image.uid}",
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_public_image_attrs(
        obj_out=ImageReadPublic(**content), db_item=db_public_image
    )


def test_read_public_image_with_conn(
    db_public_image: Image,
    client: TestClient,
) -> None:
    """Execute GET operations to read a public image with its relationships."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/images/{db_public_image.uid}",
        params={"with_conn": True},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_extended_public_image_attrs(
        obj_out=ImageReadExtendedPublic(**content), db_item=db_public_image
    )


def test_read_private_image_with_conn(
    db_private_image: Image,
    client: TestClient,
) -> None:
    """Execute GET operations to read a private image with its
    relationships."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/images/{db_private_image.uid}",
        params={"with_conn": True},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_extended_public_image_attrs(
        obj_out=ImageReadExtendedPublic(**content), db_item=db_private_image
    )


def test_read_image_short(
    db_public_image: Image,
    client: TestClient,
) -> None:
    """Execute GET operations to read the shrunk version of an image."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/images/{db_public_image.uid}", params={"short": True}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()

    # TODO
    # with pytest.raises(ValidationError):
    #     q = ImageReadShort(**content)

    validate_read_public_image_attrs(
        obj_out=ImageReadPublic(**content), db_item=db_public_image
    )


def test_read_not_existing_image(
    client: TestClient,
) -> None:
    """Execute GET operations to try to read a not existing image."""
    settings = get_settings()
    item_uuid = uuid4()
    response = client.get(
        f"{settings.API_V1_STR}/images/{item_uuid}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Image '{item_uuid}' not found"


def test_patch_image(
    db_public_image: Image,
    client: TestClient,
) -> None:
    """Execute PATCH operations to update a image.

    No access rights. Permission denied
    """
    settings = get_settings()
    data = create_random_image_patch()
    response = client.patch(
        f"{settings.API_V1_STR}/images/{db_public_image.uid}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = response.json()
    assert content["detail"] == "Not authenticated"


def test_patch_not_existing_image(
    client: TestClient,
) -> None:
    """Execute PATCH operations to update a not existing image.

    No access rights. Permission denied
    """
    settings = get_settings()
    data = create_random_image_patch()
    response = client.patch(
        f"{settings.API_V1_STR}/images/{uuid4()}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = response.json()
    assert content["detail"] == "Not authenticated"


def test_delete_image(
    db_public_image: Image,
    client: TestClient,
) -> None:
    """Execute PATCH operations to update a image.

    No access rights. Permission denied
    """
    settings = get_settings()
    response = client.delete(f"{settings.API_V1_STR}/images/{db_public_image.uid}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = response.json()
    assert content["detail"] == "Not authenticated"


def test_delete_not_existing_image(
    client: TestClient,
) -> None:
    """Execute PATCH operations to update a not existing image.

    No access rights. Permission denied
    """
    settings = get_settings()
    response = client.delete(f"{settings.API_V1_STR}/images/{uuid4()}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = response.json()
    assert content["detail"] == "Not authenticated"
