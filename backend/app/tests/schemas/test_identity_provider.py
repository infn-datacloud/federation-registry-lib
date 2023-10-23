from uuid import uuid4

import pytest
from app.identity_provider.models import IdentityProvider
from app.identity_provider.schemas import (
    IdentityProviderRead,
    IdentityProviderReadPublic,
    IdentityProviderReadShort,
)
from app.identity_provider.schemas_extended import (
    IdentityProviderReadExtended,
    IdentityProviderReadExtendedPublic,
)
from app.tests.utils.identity_provider import create_random_identity_provider
from pydantic import ValidationError


def test_create_schema():
    """Create a valid 'Create' Schema."""
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
    with pytest.raises(ValidationError):
        # Can't be empty list
        a.user_groups = []


def test_read_schema(db_idp: IdentityProvider):
    """Create a valid 'Read' Schema."""
    IdentityProviderRead.from_orm(db_idp)
    IdentityProviderReadPublic.from_orm(db_idp)
    IdentityProviderReadShort.from_orm(db_idp)
    IdentityProviderReadExtended.from_orm(db_idp)
    IdentityProviderReadExtendedPublic.from_orm(db_idp)
