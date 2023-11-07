import json
from typing import Dict
from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient

from app.config import get_settings
from app.project.models import Project
from app.project.schemas import ProjectBase, ProjectRead, ProjectReadShort
from app.project.schemas_extended import ProjectReadExtended
from tests.utils.project import (
    create_random_project_patch,
    validate_read_extended_project_attrs,
    validate_read_project_attrs,
    validate_read_short_project_attrs,
)


def test_read_projects(
    db_project: Project,
    db_project2: Project,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all projects."""
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/projects/", headers=read_header)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_project.uid:
        resp_proj = content[0]
        resp_proj2 = content[1]
    else:
        resp_proj = content[1]
        resp_proj2 = content[0]

    validate_read_project_attrs(obj_out=ProjectRead(**resp_proj), db_item=db_project)
    validate_read_project_attrs(obj_out=ProjectRead(**resp_proj2), db_item=db_project2)


def test_read_projects_with_target_params(
    db_project: Project,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all projects matching specific attributes passed
    as query attributes.
    """
    settings = get_settings()

    for k in ProjectBase.__fields__.keys():
        response = client.get(
            f"{settings.API_V1_STR}/projects/",
            params={k: db_project.__getattribute__(k)},
            headers=read_header,
        )
        assert response.status_code == status.HTTP_200_OK
        content = response.json()
        assert len(content) == 1
        validate_read_project_attrs(
            obj_out=ProjectRead(**content[0]), db_item=db_project
        )


def test_read_projects_with_limit(
    db_project: Project,
    db_project2: Project,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all projects limiting the number of output
    items.
    """
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/projects/",
        params={"limit": 0},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = client.get(
        f"{settings.API_V1_STR}/projects/",
        params={"limit": 1},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1


def test_read_sorted_projects(
    db_project: Project,
    db_project2: Project,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all sorted projects."""
    settings = get_settings()
    sorted_items = sorted([db_project, db_project2], key=lambda x: x.uid)

    response = client.get(
        f"{settings.API_V1_STR}/projects/",
        params={"sort": "uid"},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = client.get(
        f"{settings.API_V1_STR}/projects/",
        params={"sort": "-uid"},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid

    response = client.get(
        f"{settings.API_V1_STR}/projects/",
        params={"sort": "uid_asc"},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = client.get(
        f"{settings.API_V1_STR}/projects/",
        params={"sort": "uid_desc"},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid


def test_read_projects_with_skip(
    db_project: Project,
    db_project2: Project,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all projects, skipping the first N entries."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/projects/",
        params={"skip": 0},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    response = client.get(
        f"{settings.API_V1_STR}/projects/",
        params={"skip": 1},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1

    response = client.get(
        f"{settings.API_V1_STR}/projects/",
        params={"skip": 2},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = client.get(
        f"{settings.API_V1_STR}/projects/",
        params={"skip": 3},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_projects_with_pagination(
    db_project: Project,
    db_project2: Project,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all projects.

    Paginate returned list.
    """
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/projects/",
        params={"size": 1},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    if content[0]["uid"] == db_project.uid:
        next_page_uid = db_project2.uid
    else:
        next_page_uid = db_project.uid

    response = client.get(
        f"{settings.API_V1_STR}/projects/",
        params={"size": 1, "page": 1},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    assert content[0]["uid"] == next_page_uid

    # Page greater than 0 but size equals None, does nothing
    response = client.get(
        f"{settings.API_V1_STR}/projects/",
        params={"page": 1},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    # Page index greater than maximum number of pages. Return nothing
    response = client.get(
        f"{settings.API_V1_STR}/projects/",
        params={"size": 1, "page": 2},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_projects_with_conn(
    db_project: Project,
    db_project2: Project,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all projects with their relationships."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/projects/",
        params={"with_conn": True},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_project.uid:
        resp_proj = content[0]
        resp_proj2 = content[1]
    else:
        resp_proj = content[1]
        resp_proj2 = content[0]

    validate_read_extended_project_attrs(
        obj_out=ProjectReadExtended(**resp_proj), db_item=db_project
    )
    validate_read_extended_project_attrs(
        obj_out=ProjectReadExtended(**resp_proj2), db_item=db_project2
    )


def test_read_projects_short(
    db_project: Project,
    db_project2: Project,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all projects with their shrunk version."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/projects/",
        params={"short": True},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_project.uid:
        resp_proj = content[0]
        resp_proj2 = content[1]
    else:
        resp_proj = content[1]
        resp_proj2 = content[0]

    validate_read_short_project_attrs(
        obj_out=ProjectReadShort(**resp_proj), db_item=db_project
    )
    validate_read_short_project_attrs(
        obj_out=ProjectReadShort(**resp_proj2), db_item=db_project2
    )


def test_read_project(
    db_project: Project,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read a project."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/projects/{db_project.uid}", headers=read_header
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_project_attrs(obj_out=ProjectRead(**content), db_item=db_project)


def test_read_project_with_conn(
    db_project: Project,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read a project with its relationships."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/projects/{db_project.uid}",
        params={"with_conn": True},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_extended_project_attrs(
        obj_out=ProjectReadExtended(**content), db_item=db_project
    )


def test_read_project_short(
    db_project: Project,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read the shrunk version of a project."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/projects/{db_project.uid}",
        params={"short": True},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_short_project_attrs(
        obj_out=ProjectReadShort(**content), db_item=db_project
    )


def test_read_not_existing_project(
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to try to read a not existing project."""
    settings = get_settings()
    item_uuid = uuid4()
    response = client.get(
        f"{settings.API_V1_STR}/projects/{item_uuid}", headers=read_header
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Project '{item_uuid}' not found"


def test_patch_project(
    db_project: Project,
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute PATCH operations to update a project."""
    settings = get_settings()
    data = create_random_project_patch()

    response = client.patch(
        f"{settings.API_V1_STR}/projects/{db_project.uid}",
        json=json.loads(data.json()),
        headers=write_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    for k, v in data.dict().items():
        assert content[k] == v


def test_patch_project_no_edit(
    db_project: Project, client: TestClient, write_header: Dict
) -> None:
    """Execute PATCH operations to update a project.

    Nothing changes.
    """
    settings = get_settings()
    data = create_random_project_patch(default=True)

    response = client.patch(
        f"{settings.API_V1_STR}/projects/{db_project.uid}",
        json=json.loads(data.json(exclude_unset=True)),
        headers=write_header,
    )
    assert response.status_code == status.HTTP_304_NOT_MODIFIED


def test_patch_not_existing_project(
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute PATCH operations to try to update a not existing project."""
    settings = get_settings()
    item_uuid = uuid4()
    data = create_random_project_patch()

    response = client.patch(
        f"{settings.API_V1_STR}/projects/{item_uuid}",
        json=json.loads(data.json()),
        headers=write_header,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Project '{item_uuid}' not found"


def test_patch_project_with_duplicated_uuid_same_provider(
    db_project2: Project,
    db_project3: Project,
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute PATCH operations to try to assign an already existing UUID to a project
    belonging to the same provider.
    """
    settings = get_settings()
    data = create_random_project_patch()
    data.uuid = db_project2.uuid

    response = client.patch(
        f"{settings.API_V1_STR}/projects/{db_project3.uid}",
        json=json.loads(data.json()),
        headers=write_header,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    content = response.json()
    assert content["detail"] == f"Project with uuid '{data.uuid}' already registered"


def test_patch_project_with_duplicated_uuid_diff_provider(
    db_project: Project,
    db_project3: Project,
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute PATCH operations to assign an already existing UUID to a project
    belonging to a different provider.
    """
    settings = get_settings()
    data = create_random_project_patch()
    data.uuid = db_project.uuid

    response = client.patch(
        f"{settings.API_V1_STR}/projects/{db_project3.uid}",
        json=json.loads(data.json()),
        headers=write_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    for k, v in data.dict().items():
        assert content[k] == v


def test_patch_project_with_duplicated_name_same_provider(
    db_project2: Project,
    db_project3: Project,
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute PATCH operations to try to assign a name already in use to a project
    belonging to the same provider.
    """
    settings = get_settings()
    data = create_random_project_patch()
    data.name = db_project2.name

    response = client.patch(
        f"{settings.API_V1_STR}/projects/{db_project3.uid}",
        json=json.loads(data.json()),
        headers=write_header,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    content = response.json()
    assert content["detail"] == f"Project with name '{data.name}' already registered"


def test_patch_project_with_duplicated_name_diff_provider(
    db_project: Project,
    db_project3: Project,
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute PATCH operations to assign an already existing UUID to a project
    belonging to a different provider.
    """
    settings = get_settings()
    data = create_random_project_patch()
    data.name = db_project.name

    response = client.patch(
        f"{settings.API_V1_STR}/projects/{db_project3.uid}",
        json=json.loads(data.json()),
        headers=write_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    for k, v in data.dict().items():
        assert content[k] == v


# TODO Add tests raising 422


def test_delete_project(
    db_project: Project,
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute DELETE to remove a project."""
    settings = get_settings()
    response = client.delete(
        f"{settings.API_V1_STR}/projects/{db_project.uid}",
        headers=write_header,
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_not_existing_project(
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute DELETE operations to try to delete a not existing project."""
    settings = get_settings()
    item_uuid = uuid4()
    response = client.delete(
        f"{settings.API_V1_STR}/projects/{item_uuid}", headers=write_header
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Project '{item_uuid}' not found"
