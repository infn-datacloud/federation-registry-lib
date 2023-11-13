import pytest

from app.identity_provider.crud import identity_provider
from app.identity_provider.models import IdentityProvider
from app.provider.models import Provider
from tests.utils.identity_provider import create_random_identity_provider


@pytest.fixture
def db_idp_with_single_user_group(
    db_provider_with_single_project: Provider,
) -> IdentityProvider:
    """Identity Provider with a single user group.

    It is linked to the provider with only one project.
    """
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider_with_single_project.projects]
    )
    item = identity_provider.create(
        obj_in=item_in, provider=db_provider_with_single_project
    )
    yield item


@pytest.fixture
def db_idp_with_multiple_user_groups(
    db_provider_with_multiple_projects: Provider,
) -> IdentityProvider:
    """Identity Provider with multiple user groups.

    It is linked to the provider with multiple projects and generates a user group for
    each provider project.
    """
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider_with_multiple_projects.projects]
    )
    item = identity_provider.create(
        obj_in=item_in, provider=db_provider_with_multiple_projects
    )
    yield item


@pytest.fixture
def db_idp_with_multiple_providers(
    db_provider_with_single_project: Provider,
    db_provider_with_multiple_projects: Provider,
) -> IdentityProvider:
    """Identity Provider with multiple user groups, linked to multiple providers.

    It has a user group on a provider and 2 user groups on the other one. Each user
    group points to exactly one project.
    """
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider_with_single_project.projects]
    )
    item = identity_provider.create(
        obj_in=item_in, provider=db_provider_with_single_project
    )
    item_in.user_groups = create_random_identity_provider(
        projects=[i.uuid for i in db_provider_with_multiple_projects.projects]
    ).user_groups
    item = identity_provider.create(
        obj_in=item_in, provider=db_provider_with_multiple_projects
    )
    yield item


@pytest.fixture
def db_provider_with_single_idp(
    db_idp_with_single_user_group: IdentityProvider,
) -> Provider:
    """Provider with a single authorized IDP and a single project."""
    return db_idp_with_single_user_group.providers.single()


@pytest.fixture
def db_provider_with_multiple_idps(
    db_provider_with_multiple_projects: Provider,
) -> Provider:
    """Provider with a multiple authorized IDP and multiple projects.

    Each IDP has a single user group. Each user group points to a different project.
    """
    db_project1 = db_provider_with_multiple_projects.projects.single()
    db_project2 = db_provider_with_multiple_projects.projects.all()[1]
    item_in = create_random_identity_provider(projects=[db_project1.uuid])
    identity_provider.create(
        obj_in=item_in, provider=db_provider_with_multiple_projects
    )
    item_in = create_random_identity_provider(projects=[db_project2.uuid])
    identity_provider.create(
        obj_in=item_in, provider=db_provider_with_multiple_projects
    )
    yield db_provider_with_multiple_projects


@pytest.fixture
def db_provider_with_shared_idp(
    db_idp_with_multiple_providers: IdentityProvider,
) -> Provider:
    yield db_idp_with_multiple_providers.providers.single()
