"""Provider specific fixtures."""
from pytest_cases import fixture, fixture_union, parametrize

from app.provider.crud import provider_mng
from app.provider.models import Provider
from app.provider.schemas_extended import (
    ProviderCreateExtended,
)
from tests.identity_provider.utils import (
    random_identity_provider_required_attr,
    random_identity_provider_required_rel,
)
from tests.project.utils import random_project_required_attr
from tests.provider.utils import (
    random_provider_all_no_default_attr,
    random_provider_required_attr,
)
from tests.region.utils import random_region_required_attr


@fixture
def db_provider_simple() -> Provider:
    """Fixture with standard DB Provider."""
    item = ProviderCreateExtended(**random_provider_required_attr())
    return provider_mng.create(obj_in=item)


@fixture
def db_provider_no_defaults() -> Provider:
    """Fixture with standard DB Provider."""
    item = ProviderCreateExtended(**random_provider_all_no_default_attr())
    return provider_mng.create(obj_in=item)


@fixture
@parametrize(owned_regions=[1, 2])
def db_provider_with_regions(owned_regions: int) -> Provider:
    """Fixture with standard DB Provider."""
    item = ProviderCreateExtended(
        **random_provider_required_attr(),
        regions=[random_region_required_attr() for _ in range(owned_regions)],
    )
    return provider_mng.create(obj_in=item)


@fixture
def db_provider_with_single_project() -> Provider:
    """Fixture with standard DB Provider."""
    item = ProviderCreateExtended(
        **random_provider_required_attr(), projects=[random_project_required_attr()]
    )
    return provider_mng.create(obj_in=item)


@fixture
def db_provider_with_projects() -> Provider:
    """Fixture with standard DB Provider."""
    item = ProviderCreateExtended(
        **random_provider_required_attr(),
        projects=[random_project_required_attr(), random_project_required_attr()],
    )
    return provider_mng.create(obj_in=item)


@fixture
@parametrize(owned_identity_providers=[1, 2])
def db_provider_with_idps(owned_identity_providers: int) -> Provider:
    """Fixture with standard DB Provider."""
    projects = [random_project_required_attr() for _ in range(owned_identity_providers)]
    identity_providers = []
    for project in projects:
        relationships = random_identity_provider_required_rel()
        relationships["user_groups"][0]["sla"]["project"] = project["uuid"]
        identity_providers.append(
            {**random_identity_provider_required_attr(), **relationships}
        )
    item = ProviderCreateExtended(
        **random_provider_required_attr(),
        projects=projects,
        identity_providers=identity_providers,
    )
    return provider_mng.create(obj_in=item)


db_provider = fixture_union(
    "db_provider",
    (
        db_provider_simple,
        db_provider_with_regions,
        db_provider_with_projects,
        db_provider_with_idps,
    ),
    idstyle="explicit",
)
