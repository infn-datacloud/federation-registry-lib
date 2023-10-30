from uuid import uuid4

import pytest
from app.flavor.models import Flavor
from app.flavor.schemas import FlavorRead, FlavorReadPublic, FlavorReadShort
from app.flavor.schemas_extended import FlavorReadExtended, FlavorReadExtendedPublic
from pydantic import ValidationError
from tests.utils.flavor import (
    create_random_flavor,
    validate_read_extended_flavor_attrs,
    validate_read_extended_public_flavor_attrs,
    validate_read_flavor_attrs,
    validate_read_public_flavor_attrs,
    validate_read_short_flavor_attrs,
)


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


def test_read_schema_public_flavor(db_public_flavor: Flavor):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target flavor is linked to a single service.
    """
    schema = FlavorRead.from_orm(db_public_flavor)
    validate_read_flavor_attrs(obj_out=schema, db_item=db_public_flavor)
    schema = FlavorReadShort.from_orm(db_public_flavor)
    validate_read_short_flavor_attrs(obj_out=schema, db_item=db_public_flavor)
    schema = FlavorReadPublic.from_orm(db_public_flavor)
    validate_read_public_flavor_attrs(obj_out=schema, db_item=db_public_flavor)
    schema = FlavorReadExtended.from_orm(db_public_flavor)
    validate_read_extended_flavor_attrs(obj_out=schema, db_item=db_public_flavor)
    schema = FlavorReadExtendedPublic.from_orm(db_public_flavor)
    validate_read_extended_public_flavor_attrs(obj_out=schema, db_item=db_public_flavor)


def test_read_schema_private_flavor_single_project(db_private_flavor: Flavor):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target flavor is linked to a single service and owned by a single
    project.
    """
    schema = FlavorRead.from_orm(db_private_flavor)
    validate_read_flavor_attrs(obj_out=schema, db_item=db_private_flavor)
    schema = FlavorReadShort.from_orm(db_private_flavor)
    validate_read_short_flavor_attrs(obj_out=schema, db_item=db_private_flavor)
    schema = FlavorReadPublic.from_orm(db_private_flavor)
    validate_read_public_flavor_attrs(obj_out=schema, db_item=db_private_flavor)
    schema = FlavorReadExtended.from_orm(db_private_flavor)
    validate_read_extended_flavor_attrs(obj_out=schema, db_item=db_private_flavor)
    schema = FlavorReadExtendedPublic.from_orm(db_private_flavor)
    validate_read_extended_public_flavor_attrs(
        obj_out=schema, db_item=db_private_flavor
    )


def test_read_schema_private_flavor_multiple_projects(
    db_private_flavor_multiple_projects: Flavor,
):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target flavor is linked to a single service and owned by multiple
    projects on the same provider.
    """
    schema = FlavorRead.from_orm(db_private_flavor_multiple_projects)
    validate_read_flavor_attrs(
        obj_out=schema, db_item=db_private_flavor_multiple_projects
    )
    schema = FlavorReadShort.from_orm(db_private_flavor_multiple_projects)
    validate_read_short_flavor_attrs(
        obj_out=schema, db_item=db_private_flavor_multiple_projects
    )
    schema = FlavorReadPublic.from_orm(db_private_flavor_multiple_projects)
    validate_read_public_flavor_attrs(
        obj_out=schema, db_item=db_private_flavor_multiple_projects
    )
    schema = FlavorReadExtended.from_orm(db_private_flavor_multiple_projects)
    assert len(schema.projects) > 1
    validate_read_extended_flavor_attrs(
        obj_out=schema, db_item=db_private_flavor_multiple_projects
    )
    schema = FlavorReadExtendedPublic.from_orm(db_private_flavor_multiple_projects)
    assert len(schema.projects) > 1
    validate_read_extended_public_flavor_attrs(
        obj_out=schema, db_item=db_private_flavor_multiple_projects
    )


def test_read_schema_flavor_shared_between_multiple_services(db_shared_flavor: Flavor):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target public flavor is linked to a multiple services.
    """
    schema = FlavorRead.from_orm(db_shared_flavor)
    validate_read_flavor_attrs(obj_out=schema, db_item=db_shared_flavor)
    schema = FlavorReadShort.from_orm(db_shared_flavor)
    validate_read_short_flavor_attrs(obj_out=schema, db_item=db_shared_flavor)
    schema = FlavorReadPublic.from_orm(db_shared_flavor)
    validate_read_public_flavor_attrs(obj_out=schema, db_item=db_shared_flavor)
    schema = FlavorReadExtended.from_orm(db_shared_flavor)
    assert len(schema.services) > 1
    validate_read_extended_flavor_attrs(obj_out=schema, db_item=db_shared_flavor)
    schema = FlavorReadExtendedPublic.from_orm(db_shared_flavor)
    assert len(schema.services) > 1
    validate_read_extended_public_flavor_attrs(obj_out=schema, db_item=db_shared_flavor)
