from uuid import uuid4

import pytest
from pydantic import ValidationError

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
from tests.utils.identity_provider import (
    create_random_identity_provider,
    validate_read_extended_identity_provider_attrs,
    validate_read_extended_public_identity_provider_attrs,
    validate_read_identity_provider_attrs,
    validate_read_public_identity_provider_attrs,
    validate_read_short_identity_provider_attrs,
)


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


def test_read_schema_with_single_user_group(
    db_idp_with_single_user_group: IdentityProvider,
):
    """Create a valid 'Read' Schema from DB object.

    Target IDP has one user group.

    Apply conversion for this item for all read schemas. No one of them should raise
    errors.
    """
    schema = IdentityProviderRead.from_orm(db_idp_with_single_user_group)
    validate_read_identity_provider_attrs(
        obj_out=schema, db_item=db_idp_with_single_user_group
    )
    schema = IdentityProviderReadShort.from_orm(db_idp_with_single_user_group)
    validate_read_short_identity_provider_attrs(
        obj_out=schema, db_item=db_idp_with_single_user_group
    )
    schema = IdentityProviderReadPublic.from_orm(db_idp_with_single_user_group)
    validate_read_public_identity_provider_attrs(
        obj_out=schema, db_item=db_idp_with_single_user_group
    )
    schema = IdentityProviderReadExtended.from_orm(db_idp_with_single_user_group)
    validate_read_extended_identity_provider_attrs(
        obj_out=schema, db_item=db_idp_with_single_user_group
    )
    schema = IdentityProviderReadExtendedPublic.from_orm(db_idp_with_single_user_group)
    validate_read_extended_public_identity_provider_attrs(
        obj_out=schema, db_item=db_idp_with_single_user_group
    )


def test_read_schema_with_multiple_user_groups(
    db_idp_with_multiple_user_groups: IdentityProvider,
):
    """Create a valid 'Read' Schema from DB object.

    Target IDP has multiple user groups.

    Apply conversion for this item for all read schemas. No one of them should raise
    errors.
    """
    schema = IdentityProviderRead.from_orm(db_idp_with_multiple_user_groups)
    validate_read_identity_provider_attrs(
        obj_out=schema, db_item=db_idp_with_multiple_user_groups
    )
    schema = IdentityProviderReadShort.from_orm(db_idp_with_multiple_user_groups)
    validate_read_short_identity_provider_attrs(
        obj_out=schema, db_item=db_idp_with_multiple_user_groups
    )
    schema = IdentityProviderReadPublic.from_orm(db_idp_with_multiple_user_groups)
    validate_read_public_identity_provider_attrs(
        obj_out=schema, db_item=db_idp_with_multiple_user_groups
    )
    schema = IdentityProviderReadExtended.from_orm(db_idp_with_multiple_user_groups)
    assert len(schema.user_groups) > 1
    validate_read_extended_identity_provider_attrs(
        obj_out=schema, db_item=db_idp_with_multiple_user_groups
    )
    schema = IdentityProviderReadExtendedPublic.from_orm(
        db_idp_with_multiple_user_groups
    )
    assert len(schema.user_groups) > 1
    validate_read_extended_public_identity_provider_attrs(
        obj_out=schema, db_item=db_idp_with_multiple_user_groups
    )


def test_read_schema_with_multiple_providers(
    db_idp_with_multiple_providers: IdentityProvider,
):
    """Create a valid 'Read' Schema from DB object.

    Target IDP has multiple user groups, one for each provider.

    Apply conversion for this item for all read schemas. No one of them should raise
    errors.
    """
    schema = IdentityProviderRead.from_orm(db_idp_with_multiple_providers)
    validate_read_identity_provider_attrs(
        obj_out=schema, db_item=db_idp_with_multiple_providers
    )
    schema = IdentityProviderReadShort.from_orm(db_idp_with_multiple_providers)
    validate_read_short_identity_provider_attrs(
        obj_out=schema, db_item=db_idp_with_multiple_providers
    )
    schema = IdentityProviderReadPublic.from_orm(db_idp_with_multiple_providers)
    validate_read_public_identity_provider_attrs(
        obj_out=schema, db_item=db_idp_with_multiple_providers
    )
    schema = IdentityProviderReadExtended.from_orm(db_idp_with_multiple_providers)
    assert len(schema.providers) > 1
    validate_read_extended_identity_provider_attrs(
        obj_out=schema, db_item=db_idp_with_multiple_providers
    )
    schema = IdentityProviderReadExtendedPublic.from_orm(db_idp_with_multiple_providers)
    assert len(schema.providers) > 1
    validate_read_extended_public_identity_provider_attrs(
        obj_out=schema, db_item=db_idp_with_multiple_providers
    )
