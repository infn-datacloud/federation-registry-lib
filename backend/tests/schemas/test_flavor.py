from uuid import uuid4

import pytest
from app.flavor.crud import flavor
from app.flavor.schemas import FlavorRead, FlavorReadPublic, FlavorReadShort
from app.flavor.schemas_extended import FlavorReadExtended, FlavorReadExtendedPublic
from app.service.models import ComputeService
from pydantic import ValidationError
from tests.utils.flavor import create_random_flavor


def test_create_schema():
    """Create a valid 'Create' Schema."""
    create_random_flavor()
    create_random_flavor(default=True)
    create_random_flavor(projects=[uuid4()])
    create_random_flavor(default=True, projects=[uuid4()])


def test_invalid_create_schema():
    """List all invalid situations for a 'Create' Schema."""
    a = create_random_flavor(projects=[uuid4()])
    with pytest.raises(ValidationError):
        a.uuid = None
    with pytest.raises(ValidationError):
        a.name = None
    with pytest.raises(ValidationError):
        a.disk = -1
    with pytest.raises(ValidationError):
        a.ram = -1
    with pytest.raises(ValidationError):
        a.vcpus = -1
    with pytest.raises(ValidationError):
        a.swap = -1
    with pytest.raises(ValidationError):
        a.ephemeral = -1
    with pytest.raises(ValidationError):
        # Num GPUs is 0 when GPU model or GPU vendor are not None
        assert a.gpu_model or a.gpu_vendor
        a.gpus = 0
    with pytest.raises(ValidationError):
        # Empty projects list when the flavor is private
        assert not a.is_public
        a.projects = []
    with pytest.raises(ValidationError):
        # Public flavor with projects
        assert len(a.projects) > 0
        a.is_public = True
    with pytest.raises(ValidationError):
        # Duplicated projects
        a.projects = [a.projects[0], a.projects[0]]


def test_read_schema(db_compute_serv: ComputeService):
    """Create a valid 'Read' Schema."""
    obj_in = create_random_flavor()
    db_obj = flavor.create(obj_in=obj_in, service=db_compute_serv)
    FlavorRead.from_orm(db_obj)
    FlavorReadPublic.from_orm(db_obj)
    FlavorReadShort.from_orm(db_obj)
    FlavorReadExtended.from_orm(db_obj)
    FlavorReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_flavor(default=True)
    db_obj = flavor.create(obj_in=obj_in, service=db_compute_serv)
    FlavorRead.from_orm(db_obj)
    FlavorReadPublic.from_orm(db_obj)
    FlavorReadShort.from_orm(db_obj)
    FlavorReadExtended.from_orm(db_obj)
    FlavorReadExtendedPublic.from_orm(db_obj)

    db_region = db_compute_serv.region.single()
    db_provider = db_region.provider.single()
    obj_in = create_random_flavor(projects=[i.uuid for i in db_provider.projects])
    db_obj = flavor.create(obj_in=obj_in, service=db_compute_serv)
    FlavorRead.from_orm(db_obj)
    FlavorReadPublic.from_orm(db_obj)
    FlavorReadShort.from_orm(db_obj)
    FlavorReadExtended.from_orm(db_obj)
    FlavorReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_flavor(
        default=True, projects=[i.uuid for i in db_provider.projects]
    )
    db_obj = flavor.create(obj_in=obj_in, service=db_compute_serv)
    FlavorRead.from_orm(db_obj)
    FlavorReadPublic.from_orm(db_obj)
    FlavorReadShort.from_orm(db_obj)
    FlavorReadExtended.from_orm(db_obj)
    FlavorReadExtendedPublic.from_orm(db_obj)
