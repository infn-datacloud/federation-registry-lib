import pytest

from app.identity_provider.crud import identity_provider
from app.identity_provider.models import IdentityProvider
from app.provider.models import Provider
from app.user_group.models import UserGroup
from tests.utils.identity_provider import create_random_identity_provider


@pytest.fixture
def db_user_group(db_idp_with_single_user_group: IdentityProvider) -> UserGroup:
    """User group owned by the idp with just one user group.

    It has just one SLA.
    """
    yield db_idp_with_single_user_group.user_groups.single()


@pytest.fixture
def db_user_group2(db_idp_with_multiple_user_groups: IdentityProvider) -> UserGroup:
    """First user group owned by the idp with multiple user groups.

    It has just one SLA.
    """
    yield db_idp_with_multiple_user_groups.user_groups.single()


@pytest.fixture
def db_user_group3(db_idp_with_multiple_user_groups: IdentityProvider) -> UserGroup:
    """Second user group owned by the idp with multiple user groups.

    It has just one SLA.
    """
    yield db_idp_with_multiple_user_groups.user_groups.all()[1]


@pytest.fixture
def db_user_group_with_multiple_slas(
    db_provider_with_single_project: Provider,
    db_provider_with_multiple_projects: Provider,
) -> UserGroup:
    """User Group with multiple SLAs.

    Each SLA points to a project belonging to a different provider.
    """
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider_with_single_project.projects]
    )
    item = identity_provider.create(
        obj_in=item_in, provider=db_provider_with_single_project
    )
    item_in.user_groups[0].sla = (
        create_random_identity_provider(
            projects=[i.uuid for i in db_provider_with_multiple_projects.projects]
        )
        .user_groups[0]
        .sla
    )
    item = identity_provider.create(
        obj_in=item_in, provider=db_provider_with_multiple_projects
    )
    yield item.user_groups.single()
