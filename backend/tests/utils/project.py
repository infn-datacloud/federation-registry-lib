from uuid import uuid4

from app.project.models import Project
from app.project.schemas import (
    ProjectBase,
    ProjectCreate,
    ProjectRead,
    ProjectReadPublic,
    ProjectReadShort,
    ProjectUpdate,
)
from app.project.schemas_extended import ProjectReadExtended, ProjectReadExtendedPublic
from tests.utils.utils import random_lower_string


def create_random_project(default: bool = False) -> ProjectCreate:
    name = random_lower_string()
    uuid = uuid4()
    kwargs = {}
    if not default:
        kwargs = {"description": random_lower_string()}
    return ProjectCreate(name=name, uuid=uuid, **kwargs)


def create_random_project_patch(default: bool = False) -> ProjectUpdate:
    if default:
        return ProjectUpdate()
    description = random_lower_string()
    name = random_lower_string()
    uuid = uuid4()
    return ProjectUpdate(description=description, name=name, uuid=uuid)


def validate_project_attrs(*, obj_in: ProjectBase, db_item: Project) -> None:
    assert db_item.description == obj_in.description
    assert db_item.name == obj_in.name
    assert db_item.uuid == obj_in.uuid


def validate_project_public_attrs(*, obj_in: ProjectBase, db_item: Project) -> None:
    assert db_item.description == obj_in.description
    assert db_item.name == obj_in.name
    assert db_item.uuid == obj_in.uuid


def validate_create_project_attrs(*, obj_in: ProjectCreate, db_item: Project) -> None:
    validate_project_attrs(obj_in=obj_in, db_item=db_item)


def validate_read_project_attrs(*, obj_out: ProjectRead, db_item: Project) -> None:
    assert db_item.uid == obj_out.uid
    validate_project_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_short_project_attrs(
    *, obj_out: ProjectReadShort, db_item: Project
) -> None:
    assert db_item.uid == obj_out.uid
    validate_project_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_public_project_attrs(
    *, obj_out: ProjectReadPublic, db_item: Project
) -> None:
    assert db_item.uid == obj_out.uid
    validate_project_public_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_extended_project_attrs(
    *, obj_out: ProjectReadExtended, db_item: Project
) -> None:
    assert db_item.uid == obj_out.uid
    validate_project_attrs(obj_in=obj_out, db_item=db_item)
    assert len(db_item.private_networks) == len(obj_out.private_networks)
    for db_net, net_out in zip(db_item.private_networks, obj_out.private_networks):
        assert db_net.uid == net_out.uid
    assert len(db_item.private_flavors) == len(obj_out.private_flavors)
    for db_net, net_out in zip(db_item.private_flavors, obj_out.private_flavors):
        assert db_net.uid == net_out.uid
    assert len(db_item.private_images) == len(obj_out.private_images)
    for db_net, net_out in zip(db_item.private_images, obj_out.private_images):
        assert db_net.uid == net_out.uid
    assert len(db_item.quotas) == len(obj_out.quotas)
    for db_net, net_out in zip(db_item.quotas, obj_out.quotas):
        assert db_net.uid == net_out.uid
    db_provider = db_item.provider.single()
    assert db_provider
    assert db_provider.uid == obj_out.provider.uid
    db_sla = db_item.sla.single()
    if db_sla:
        assert db_sla.uid == obj_out.sla.uid
    else:
        assert not obj_out.sla


def validate_read_extended_public_project_attrs(
    *, obj_out: ProjectReadExtendedPublic, db_item: Project
) -> None:
    assert db_item.uid == obj_out.uid
    validate_project_public_attrs(obj_in=obj_out, db_item=db_item)
    assert len(db_item.private_networks) == len(obj_out.private_networks)
    for db_net, net_out in zip(db_item.private_networks, obj_out.private_networks):
        assert db_net.uid == net_out.uid
    assert len(db_item.private_flavors) == len(obj_out.private_flavors)
    for db_net, net_out in zip(db_item.private_flavors, obj_out.private_flavors):
        assert db_net.uid == net_out.uid
    assert len(db_item.private_images) == len(obj_out.private_images)
    for db_net, net_out in zip(db_item.private_images, obj_out.private_images):
        assert db_net.uid == net_out.uid
    assert len(db_item.quotas) == len(obj_out.quotas)
    for db_net, net_out in zip(db_item.quotas, obj_out.quotas):
        assert db_net.uid == net_out.uid
    db_provider = db_item.provider.single()
    assert db_provider
    assert db_provider.uid == obj_out.provider.uid
    db_sla = db_item.sla.single()
    if db_sla:
        assert db_sla.uid == obj_out.sla.uid
    else:
        assert not obj_out.sla
