from typing import Generator
from uuid import uuid4

from app.tests.utils.project import (
    create_random_project,
    create_random_update_project_data,
)
from app.tests.utils.utils import random_lower_string
from app.project.crud import project
from app.project.schemas import ProjectCreate


def test_create_item(setup_and_teardown_db: Generator) -> None:
    description = random_lower_string()
    name = random_lower_string()
    uuid = uuid4()
    public_network_name = random_lower_string()
    private_network_name = random_lower_string()
    private_network_proxy_host = random_lower_string()
    private_network_proxy_user = random_lower_string()
    item_in = ProjectCreate(
        description=description,
        name=name,
        uuid=uuid,
        public_network_name=public_network_name,
        private_network_name=private_network_name,
        private_network_proxy_host=private_network_proxy_host,
        private_network_proxy_user=private_network_proxy_user,
    )
    item = project.create(obj_in=item_in)
    assert item.description == description
    assert item.name == name
    assert item.uuid == str(uuid)
    assert item.public_network_name == public_network_name
    assert item.private_network_name == private_network_name
    assert item.private_network_proxy_host == private_network_proxy_host
    assert item.private_network_proxy_user == private_network_proxy_user


def test_create_item_default_values(setup_and_teardown_db: Generator) -> None:
    name = random_lower_string()
    uuid = uuid4()
    item_in = ProjectCreate(name=name, uuid=uuid)
    item = project.create(obj_in=item_in)
    assert item.description == ""
    assert item.name == name
    assert item.uuid == str(uuid)
    assert item.public_network_name is None
    assert item.private_network_name is None
    assert item.private_network_proxy_host is None
    assert item.private_network_proxy_user is None


def test_get_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_project()
    stored_item = project.get(uid=item.uid)
    assert stored_item
    assert item.uid == stored_item.uid
    assert item.description == stored_item.description
    assert item.public_network_name == stored_item.public_network_name
    assert item.private_network_name == stored_item.private_network_name
    assert (
        item.private_network_proxy_host
        == stored_item.private_network_proxy_host
    )
    assert (
        item.private_network_proxy_user
        == stored_item.private_network_proxy_user
    )


def test_get_items(setup_and_teardown_db: Generator) -> None:
    item = create_random_project()
    item2 = create_random_project()
    stored_items = project.get_multi()
    assert len(stored_items) == 2

    stored_items = project.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = project.get_multi(uid=item.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == item.uid
    assert stored_items[0].description == item.description
    assert stored_items[0].public_network_name == item.public_network_name
    assert stored_items[0].private_network_name == item.private_network_name
    assert (
        stored_items[0].private_network_proxy_host
        == item.private_network_proxy_host
    )
    assert (
        stored_items[0].private_network_proxy_user
        == item.private_network_proxy_user
    )

    sorted_items = list(sorted([item, item2], key=lambda x: x.uid))
    stored_items = project.get_multi(sort="uid")
    assert stored_items[0].uid == sorted_items[0].uid
    assert stored_items[1].uid == sorted_items[1].uid
    stored_items = project.get_multi(sort="-uid")
    assert stored_items[0].uid == sorted_items[1].uid
    assert stored_items[1].uid == sorted_items[0].uid


def test_update_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_project()
    item_update = create_random_update_project_data()
    item2 = project.update(db_obj=item, obj_in=item_update)
    assert item2.uid == item.uid
    assert item2.description == item_update.description
    assert item.public_network_name == item_update.public_network_name
    assert item.private_network_name == item_update.private_network_name
    assert (
        item.private_network_proxy_host
        == item_update.private_network_proxy_host
    )
    assert (
        item.private_network_proxy_user
        == item_update.private_network_proxy_user
    )

    item_update = create_random_update_project_data()
    item2 = project.update(db_obj=item, obj_in=item_update.dict())
    assert item2.uid == item.uid
    assert item2.description == item_update.description
    assert item.public_network_name == item_update.public_network_name
    assert item.private_network_name == item_update.private_network_name
    assert (
        item.private_network_proxy_host
        == item_update.private_network_proxy_host
    )
    assert (
        item.private_network_proxy_user
        == item_update.private_network_proxy_user
    )


def test_delete_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_project()
    item2 = project.remove(db_obj=item)
    item3 = project.get(uid=item.uid)
    assert item2 is True
    assert item3 is None
