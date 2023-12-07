from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.network.models import Network
from app.network.schemas import (
    NetworkRead,
    NetworkReadPublic,
)
from app.network.schemas_extended import (
    NetworkReadExtended,
    NetworkReadExtendedPublic,
)
from tests.utils.network import (
    create_random_network,
    validate_read_extended_network_attrs,
    validate_read_extended_public_network_attrs,
    validate_read_network_attrs,
    validate_read_public_network_attrs,
)


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


def test_read_schema_public_network(db_public_network: Network):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them should raise
    errors.

    Target network is linked to a single service.
    """
    schema = NetworkRead.from_orm(db_public_network)
    validate_read_network_attrs(obj_out=schema, db_item=db_public_network)
    schema = NetworkReadPublic.from_orm(db_public_network)
    validate_read_public_network_attrs(obj_out=schema, db_item=db_public_network)
    schema = NetworkReadExtended.from_orm(db_public_network)
    validate_read_extended_network_attrs(obj_out=schema, db_item=db_public_network)
    schema = NetworkReadExtendedPublic.from_orm(db_public_network)
    validate_read_extended_public_network_attrs(
        obj_out=schema, db_item=db_public_network
    )


def test_read_schema_private_network(db_private_network: Network):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them should raise
    errors.

    Target network is linked to a single service and owned by a single project.
    """
    schema = NetworkRead.from_orm(db_private_network)
    validate_read_network_attrs(obj_out=schema, db_item=db_private_network)
    schema = NetworkReadPublic.from_orm(db_private_network)
    validate_read_public_network_attrs(obj_out=schema, db_item=db_private_network)
    schema = NetworkReadExtended.from_orm(db_private_network)
    validate_read_extended_network_attrs(obj_out=schema, db_item=db_private_network)
    schema = NetworkReadExtendedPublic.from_orm(db_private_network)
    validate_read_extended_public_network_attrs(
        obj_out=schema, db_item=db_private_network
    )
