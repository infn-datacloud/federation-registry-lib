import json
from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient

from app.config import get_settings
from app.image.models import Image
from app.image.schemas import ImageBase, ImageRead, ImageReadShort
from app.image.schemas_extended import ImageReadExtended
from tests.utils.image import (
    create_random_image_patch,
    validate_read_extended_image_attrs,
    validate_read_image_attrs,
    validate_read_short_image_attrs,
)


def test_read_images(
    db_public_image: Image, db_private_image: Image, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read all images."""
    settings = get_settings()

    response = api_client_read_only.get(
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

    validate_read_image_attrs(
        obj_out=ImageRead(**resp_public_image), db_item=db_public_image
    )
    validate_read_image_attrs(
        obj_out=ImageRead(**resp_private_image), db_item=db_private_image
    )


def test_read_images_with_target_params(
    db_public_image: Image, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read all images matching specific attributes passed as
    query attributes.
    """
    settings = get_settings()

    for k in ImageBase.__fields__.keys():
        response = api_client_read_only.get(
            f"{settings.API_V1_STR}/images/",
            params={k: db_public_image.__getattribute__(k)},
        )
        assert response.status_code == status.HTTP_200_OK
        content = response.json()
        assert len(content) == 1
        validate_read_image_attrs(
            obj_out=ImageRead(**content[0]), db_item=db_public_image
        )


def test_read_images_with_limit(
    db_public_image: Image, db_private_image: Image, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read all images limiting the number of output items."""
    settings = get_settings()

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/images/", params={"limit": 0}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/images/", params={"limit": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1


def test_read_sorted_images(
    db_public_image: Image, db_private_image: Image, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read all sorted images."""
    settings = get_settings()
    sorted_items = sorted([db_public_image, db_private_image], key=lambda x: x.uid)

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/images/", params={"sort": "uid"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/images/", params={"sort": "-uid"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/images/", params={"sort": "uid_asc"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/images/", params={"sort": "uid_desc"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid


def test_read_images_with_skip(
    db_public_image: Image, db_private_image: Image, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read all images, skipping the first N entries."""
    settings = get_settings()

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/images/", params={"skip": 0}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/images/", params={"skip": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/images/", params={"skip": 2}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/images/", params={"skip": 3}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_images_with_pagination(
    db_public_image: Image, db_private_image: Image, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read all images.

    Paginate returned list.
    """
    settings = get_settings()

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/images/", params={"size": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    if content[0]["uid"] == db_public_image.uid:
        next_page_uid = db_private_image.uid
    else:
        next_page_uid = db_public_image.uid

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/images/", params={"size": 1, "page": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    assert content[0]["uid"] == next_page_uid

    # Page greater than 0 but size equals None, does nothing
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/images/", params={"page": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    # Page index greater than maximum number of pages. Return nothing
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/images/", params={"size": 1, "page": 2}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_images_with_conn(
    db_public_image: Image, db_private_image: Image, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read all images with their relationships."""
    settings = get_settings()

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/images/", params={"with_conn": True}
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

    validate_read_extended_image_attrs(
        obj_out=ImageReadExtended(**resp_public_image), db_item=db_public_image
    )
    validate_read_extended_image_attrs(
        obj_out=ImageReadExtended(**resp_private_image),
        db_item=db_private_image,
    )


def test_read_images_short(
    db_public_image: Image, db_private_image: Image, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read all images with their shrunk version."""
    settings = get_settings()

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/images/", params={"short": True}
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

    validate_read_short_image_attrs(
        obj_out=ImageReadShort(**resp_public_image), db_item=db_public_image
    )
    validate_read_short_image_attrs(
        obj_out=ImageReadShort(**resp_private_image), db_item=db_private_image
    )


def test_read_image(db_public_image: Image, api_client_read_only: TestClient) -> None:
    """Execute GET operations to read an image."""
    settings = get_settings()
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/images/{db_public_image.uid}"
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_image_attrs(obj_out=ImageRead(**content), db_item=db_public_image)


def test_read_public_image_with_conn(
    db_public_image: Image, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read a public image with its relationships."""
    settings = get_settings()
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/images/{db_public_image.uid}",
        params={"with_conn": True},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_extended_image_attrs(
        obj_out=ImageReadExtended(**content), db_item=db_public_image
    )


def test_read_private_image_with_conn(
    db_private_image: Image, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read a private image with its relationships."""
    settings = get_settings()
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/images/{db_private_image.uid}",
        params={"with_conn": True},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_extended_image_attrs(
        obj_out=ImageReadExtended(**content), db_item=db_private_image
    )


def test_read_image_short(
    db_public_image: Image, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read the shrunk version of an image."""
    settings = get_settings()
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/images/{db_public_image.uid}", params={"short": True}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_short_image_attrs(
        obj_out=ImageReadShort(**content), db_item=db_public_image
    )


def test_read_not_existing_image(api_client_read_only: TestClient) -> None:
    """Execute GET operations to try to read a not existing image."""
    settings = get_settings()
    item_uuid = uuid4()
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/images/{item_uuid}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Image '{item_uuid}' not found"


def test_patch_public_image(
    db_public_image: Image, api_client_read_write: TestClient
) -> None:
    """Execute PATCH operations to update a public image."""
    settings = get_settings()
    data = create_random_image_patch()
    data.is_public = db_public_image.is_public

    response = api_client_read_write.patch(
        f"{settings.API_V1_STR}/images/{db_public_image.uid}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    for k, v in data.dict().items():
        assert content[k] == v


def test_patch_private_image(
    db_private_image: Image, api_client_read_write: TestClient
) -> None:
    """Execute PATCH operations to update a private image."""
    settings = get_settings()
    data = create_random_image_patch()
    data.is_public = db_private_image.is_public

    response = api_client_read_write.patch(
        f"{settings.API_V1_STR}/images/{db_private_image.uid}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    for k, v in data.dict().items():
        assert content[k] == v


def test_patch_image_no_edit(
    db_public_image: Image, api_client_read_write: TestClient
) -> None:
    """Execute PATCH operations to update a image.

    Nothing changes.
    """
    settings = get_settings()
    data = create_random_image_patch(default=True)

    response = api_client_read_write.patch(
        f"{settings.API_V1_STR}/images/{db_public_image.uid}",
        json=json.loads(data.json(exclude_unset=True)),
    )
    assert response.status_code == status.HTTP_304_NOT_MODIFIED


def test_patch_not_existing_image(api_client_read_write: TestClient) -> None:
    """Execute PATCH operations to try to update a not existing image."""
    settings = get_settings()
    item_uuid = uuid4()
    data = create_random_image_patch()

    response = api_client_read_write.patch(
        f"{settings.API_V1_STR}/images/{item_uuid}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Image '{item_uuid}' not found"


def test_patch_image_changing_visibility(
    db_private_image: Image, api_client_read_write: TestClient
) -> None:
    """Execute PATCH operations to try to change the visibility of a image."""
    settings = get_settings()
    data = create_random_image_patch()
    data.is_public = not db_private_image.is_public

    response = api_client_read_write.patch(
        f"{settings.API_V1_STR}/images/{db_private_image.uid}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    content = response.json()
    assert content["detail"] == "Image visibility can't be changed"


def test_patch_image_with_duplicated_uuid(
    db_public_image: Image, db_private_image: Image, api_client_read_write: TestClient
) -> None:
    """Execute PATCH operations to try to assign an already existing UUID to a image."""
    settings = get_settings()
    data = create_random_image_patch()
    data.is_public = db_private_image.is_public
    data.uuid = db_public_image.uuid

    response = api_client_read_write.patch(
        f"{settings.API_V1_STR}/images/{db_private_image.uid}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    content = response.json()
    assert content["detail"] == f"Image with uuid '{data.uuid}' already registered"


def test_patch_image_with_duplicated_name(
    db_public_image: Image, db_private_image: Image, api_client_read_write: TestClient
) -> None:
    """Execute PATCH operations to try to assign a name already in use to a image."""
    settings = get_settings()
    data = create_random_image_patch()
    data.is_public = db_private_image.is_public
    data.name = db_public_image.name

    response = api_client_read_write.patch(
        f"{settings.API_V1_STR}/images/{db_private_image.uid}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    content = response.json()
    assert content["detail"] == f"Image with name '{data.name}' already registered"


# TODO Add tests raising 422


def test_delete_public_image(
    db_public_image: Image, api_client_read_write: TestClient
) -> None:
    """Execute DELETE to remove a public image."""
    settings = get_settings()
    response = api_client_read_write.delete(
        f"{settings.API_V1_STR}/images/{db_public_image.uid}",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_private_image(
    db_private_image: Image, api_client_read_write: TestClient
) -> None:
    """Execute DELETE to remove a private image."""
    settings = get_settings()
    response = api_client_read_write.delete(
        f"{settings.API_V1_STR}/images/{db_private_image.uid}",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_not_existing_image(api_client_read_write: TestClient) -> None:
    """Execute DELETE operations to try to delete a not existing image."""
    settings = get_settings()
    item_uuid = uuid4()
    response = api_client_read_write.delete(
        f"{settings.API_V1_STR}/images/{item_uuid}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Image '{item_uuid}' not found"
