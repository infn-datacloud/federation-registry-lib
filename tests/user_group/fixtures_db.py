"""UserGroup specific fixtures."""

from pytest_cases import fixture, fixture_union

from app.identity_provider.models import IdentityProvider
from app.user_group.models import UserGroup


@fixture
def db_user_group_simple(db_identity_provider_simple: IdentityProvider) -> UserGroup:
    """Fixture with standard DB UserGroup."""
    return db_identity_provider_simple.user_groups.single()


@fixture
def db_user_group_with_multiple_slas(
    db_shared_identity_provider: IdentityProvider,
) -> UserGroup:
    """Fixture with a UserGroup with multiple SLAs.

    Each SLA belongs to a different Provider.
    """
    db_item: UserGroup = db_shared_identity_provider.user_groups.single()
    assert len(db_item.slas) > 1
    return db_item


db_user_group = fixture_union(
    "db_user_group",
    (db_user_group_simple, db_user_group_with_multiple_slas),
    idstyle="explicit",
)
