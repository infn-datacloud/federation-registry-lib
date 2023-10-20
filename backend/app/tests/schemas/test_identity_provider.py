from uuid import uuid4

import pytest
from app.identity_provider.crud import identity_provider
from app.identity_provider.schemas import (
    IdentityProviderRead,
    IdentityProviderReadPublic,
    IdentityProviderReadShort,
)
from app.identity_provider.schemas_extended import (
    IdentityProviderReadExtended,
    IdentityProviderReadExtendedPublic,
)
from app.provider.models import Provider
from app.tests.utils.identity_provider import create_random_identity_provider
from pydantic import ValidationError


def test_create_schema():
    """Create a valid 'Create' Schema."""
    create_random_identity_provider()
    create_random_identity_provider(default=True)
    create_random_identity_provider(projects=[uuid4()])
    create_random_identity_provider(default=True, projects=[uuid4()])


def test_invalid_create_schema():
    """List all invalid situations for a 'Create' Schema."""
    a = create_random_identity_provider(projects=[uuid4()])
    with pytest.raises(ValidationError):
        a.endpoint = None
    with pytest.raises(ValidationError):
        a.group_claim = None
    with pytest.raises(ValidationError):
        a.relationship = None
    with pytest.raises(ValidationError):
        # Duplicated user groups
        a.user_groups = [a.user_groups[0], a.user_groups[0]]


def test_read_schema(db_provider_with_project: Provider):
    """Create a valid 'Read' Schema."""
    obj_in = create_random_identity_provider()
    db_obj = identity_provider.create(obj_in=obj_in, provider=db_provider_with_project)
    IdentityProviderRead.from_orm(db_obj)
    IdentityProviderReadPublic.from_orm(db_obj)
    IdentityProviderReadShort.from_orm(db_obj)
    IdentityProviderReadExtended.from_orm(db_obj)
    IdentityProviderReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_identity_provider(default=True)
    db_obj = identity_provider.create(obj_in=obj_in, provider=db_provider_with_project)
    IdentityProviderRead.from_orm(db_obj)
    IdentityProviderReadPublic.from_orm(db_obj)
    IdentityProviderReadShort.from_orm(db_obj)
    IdentityProviderReadExtended.from_orm(db_obj)
    IdentityProviderReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider_with_project.projects]
    )
    db_obj = identity_provider.create(obj_in=obj_in, provider=db_provider_with_project)
    IdentityProviderRead.from_orm(db_obj)
    IdentityProviderReadPublic.from_orm(db_obj)
    IdentityProviderReadShort.from_orm(db_obj)
    IdentityProviderReadExtended.from_orm(db_obj)
    IdentityProviderReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_identity_provider(
        default=True, projects=[i.uuid for i in db_provider_with_project.projects]
    )
    db_obj = identity_provider.create(obj_in=obj_in, provider=db_provider_with_project)
    IdentityProviderRead.from_orm(db_obj)
    IdentityProviderReadPublic.from_orm(db_obj)
    IdentityProviderReadShort.from_orm(db_obj)
    IdentityProviderReadExtended.from_orm(db_obj)
    IdentityProviderReadExtendedPublic.from_orm(db_obj)
