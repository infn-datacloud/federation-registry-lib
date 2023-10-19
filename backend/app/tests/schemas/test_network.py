from uuid import uuid4

import pytest
from app.network.crud import network
from app.network.schemas import NetworkRead, NetworkReadPublic, NetworkReadShort
from app.network.schemas_extended import NetworkReadExtended, NetworkReadExtendedPublic
from app.service.models import NetworkService
from app.tests.utils.network import create_random_network
from pydantic import ValidationError


def test_create_schema():
    """Create a valid 'Create' Schema."""
    create_random_network()
    create_random_network(default=True)
    create_random_network(project=uuid4())
    create_random_network(default=True, project=uuid4())


def test_invalid_create_schema():
    """List all invalid situations for a 'Create' Schema."""
    a = create_random_network(project=uuid4())
    with pytest.raises(ValidationError):
        a.uuid = None
    with pytest.raises(ValidationError):
        a.name = None
    with pytest.raises(ValidationError):
        # No linked project when the network is private
        assert not a.is_shared
        a.project = None
    with pytest.raises(ValidationError):
        # Public network with projects
        assert a.project
        a.is_shared = True


def test_read_schema(db_network_serv: NetworkService):
    """Create a valid 'Read' Schema."""
    obj_in = create_random_network()
    db_obj = network.create(obj_in=obj_in, service=db_network_serv)
    NetworkRead.from_orm(db_obj)
    NetworkReadPublic.from_orm(db_obj)
    NetworkReadShort.from_orm(db_obj)
    NetworkReadExtended.from_orm(db_obj)
    NetworkReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_network(default=True)
    db_obj = network.create(obj_in=obj_in, service=db_network_serv)
    NetworkRead.from_orm(db_obj)
    NetworkReadPublic.from_orm(db_obj)
    NetworkReadShort.from_orm(db_obj)
    NetworkReadExtended.from_orm(db_obj)
    NetworkReadExtendedPublic.from_orm(db_obj)

    db_region = db_network_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    obj_in = create_random_network(project=db_project.uuid)
    db_obj = network.create(obj_in=obj_in, service=db_network_serv)
    NetworkRead.from_orm(db_obj)
    NetworkReadPublic.from_orm(db_obj)
    NetworkReadShort.from_orm(db_obj)
    NetworkReadExtended.from_orm(db_obj)
    NetworkReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_network(default=True, project=db_project.uuid)
    db_obj = network.create(obj_in=obj_in, service=db_network_serv)
    NetworkRead.from_orm(db_obj)
    NetworkReadPublic.from_orm(db_obj)
    NetworkReadShort.from_orm(db_obj)
    NetworkReadExtended.from_orm(db_obj)
    NetworkReadExtendedPublic.from_orm(db_obj)
