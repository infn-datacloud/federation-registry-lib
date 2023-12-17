"""IdentityProvider specific fixtures."""
from pytest_cases import fixture, fixture_union

from app.identity_provider.crud import identity_provider_mng
from app.identity_provider.models import IdentityProvider
from app.project.models import Project
from app.provider.models import Provider
from app.provider.schemas_extended import IdentityProviderCreateExtended
from tests.identity_provider.utils import (
    random_identity_provider_required_attr,
    random_identity_provider_required_rel,
)
from tests.sla.utils import random_sla_required_attr
from tests.user_group.utils import random_user_group_required_attr


@fixture
def db_identity_provider_simple(
    db_provider_with_single_project: Provider,
) -> IdentityProvider:
    """Fixture with standard DB IdentityProvider."""
    db_project: Project = db_provider_with_single_project.projects.single()
    relationships = random_identity_provider_required_rel()
    relationships["user_groups"][0]["sla"]["project"] = db_project.uuid
    identity_provider = {**random_identity_provider_required_attr(), **relationships}
    return identity_provider_mng.create(
        obj_in=IdentityProviderCreateExtended(**identity_provider),
        provider=db_provider_with_single_project,
    )


@fixture
def db_identity_provider_multiple_user_groups(
    db_provider_with_projects: Provider,
) -> IdentityProvider:
    """Fixture with standard DB IdentityProvider."""
    user_groups = []
    for project in db_provider_with_projects.projects:
        user_groups.append(
            {
                **random_user_group_required_attr(),
                "sla": {**random_sla_required_attr(), "project": project.uuid},
            }
        )
    identity_provider = {
        **random_identity_provider_required_attr(),
        **random_identity_provider_required_rel(),
        "user_groups": user_groups,
    }
    return identity_provider_mng.create(
        obj_in=IdentityProviderCreateExtended(**identity_provider),
        provider=db_provider_with_projects,
    )


@fixture
def db_shared_identity_provider(
    db_provider_with_single_project: Provider, db_provider_with_projects: Provider
) -> IdentityProvider:
    """IdentityProvider shared within multiple providers."""
    db_project1: Project = db_provider_with_single_project.projects.single()
    db_project2: Project = db_provider_with_projects.projects.single()

    relationships = random_identity_provider_required_rel()
    relationships["user_groups"][0]["sla"]["project"] = db_project1.uuid
    identity_provider = {**random_identity_provider_required_attr(), **relationships}
    db_item = identity_provider_mng.create(
        obj_in=IdentityProviderCreateExtended(**identity_provider),
        provider=db_provider_with_single_project,
    )

    identity_provider["user_groups"][0]["sla"]["project"] = db_project2.uuid
    db_item = identity_provider_mng.create(
        obj_in=IdentityProviderCreateExtended(**identity_provider),
        provider=db_provider_with_projects,
    )

    assert len(db_item.providers) > 1
    return db_item


db_identity_provider = fixture_union(
    "db_identity_provider",
    (
        db_identity_provider_simple,
        db_identity_provider_multiple_user_groups,
        db_shared_identity_provider,
    ),
    idstyle="explicit",
)
