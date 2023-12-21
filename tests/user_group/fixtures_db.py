"""UserGroup specific fixtures."""
from pytest_cases import fixture, fixture_union

from app.identity_provider.crud import identity_provider_mng
from app.identity_provider.models import IdentityProvider
from app.project.models import Project
from app.provider.models import Provider
from app.provider.schemas_extended import IdentityProviderCreateExtended
from app.user_group.models import UserGroup
from tests.identity_provider.utils import (
    random_identity_provider_required_attr,
    random_identity_provider_required_rel,
)
from tests.sla.utils import random_sla_required_attr


@fixture
def db_user_group_simple(db_identity_provider_simple: IdentityProvider) -> UserGroup:
    """Fixture with standard DB UserGroup."""
    return db_identity_provider_simple.user_groups.single()


@fixture
def db_user_group_with_multiple_slas(
    db_provider_with_single_project: Provider, db_provider_with_projects: Provider
) -> UserGroup:
    """IdentityProvider shared within multiple providers."""
    db_project1: Project = db_provider_with_single_project.projects.single()
    db_project2: Project = db_provider_with_projects.projects.single()

    relationships = random_identity_provider_required_rel()
    relationships["user_groups"][0]["sla"]["project"] = db_project1.uuid
    identity_provider = {**random_identity_provider_required_attr(), **relationships}
    db_idp = identity_provider_mng.create(
        obj_in=IdentityProviderCreateExtended(**identity_provider),
        provider=db_provider_with_single_project,
    )

    identity_provider["user_groups"][0]["sla"] = {
        **random_sla_required_attr(),
        "project": db_project2.uuid,
    }
    db_idp = identity_provider_mng.create(
        obj_in=IdentityProviderCreateExtended(**identity_provider),
        provider=db_provider_with_projects,
    )

    db_user_group: UserGroup = db_idp.user_groups.single()
    assert len(db_idp.providers) > 1
    assert len(db_user_group.slas) > 1
    return db_user_group


db_user_group = fixture_union(
    "db_user_group",
    (db_user_group_simple, db_user_group_with_multiple_slas),
    idstyle="explicit",
)
