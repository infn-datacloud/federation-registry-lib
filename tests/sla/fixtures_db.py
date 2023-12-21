"""SLA specific fixtures."""
from pytest_cases import fixture, fixture_union

from app.identity_provider.crud import identity_provider_mng
from app.project.models import Project
from app.provider.models import Provider
from app.provider.schemas_extended import IdentityProviderCreateExtended
from app.sla.models import SLA
from app.user_group.models import UserGroup
from tests.identity_provider.utils import (
    random_identity_provider_required_attr,
    random_identity_provider_required_rel,
)
from tests.sla.utils import random_sla_required_attr
from tests.user_group.utils import random_user_group_required_attr


@fixture
def db_sla_simple(db_user_group_simple: UserGroup) -> SLA:
    """Fixture with standard DB SLA."""
    return db_user_group_simple.slas.single()


@fixture
def db_sla_with_multiple_projects(
    db_provider_with_single_project: Provider, db_provider_with_projects: Provider
) -> SLA:
    """IdentityProvider shared within multiple providers."""
    db_project1: Project = db_provider_with_single_project.projects.single()
    db_project2: Project = db_provider_with_projects.projects.single()

    user_group = {
        **random_user_group_required_attr(),
        "sla": {**random_sla_required_attr(), "project": db_project1.uuid},
    }
    identity_provider = {
        **random_identity_provider_required_attr(),
        **random_identity_provider_required_rel(),
        "user_groups": [user_group],
    }
    db_idp = identity_provider_mng.create(
        obj_in=IdentityProviderCreateExtended(**identity_provider),
        provider=db_provider_with_single_project,
    )

    user_group["sla"]["project"] = db_project2.uuid
    identity_provider["user_groups"] = [user_group]
    db_idp = identity_provider_mng.create(
        obj_in=IdentityProviderCreateExtended(**identity_provider),
        provider=db_provider_with_projects,
    )

    db_user_group: UserGroup = db_idp.user_groups.single()
    db_sla: SLA = db_user_group.slas.single()
    assert len(db_idp.providers) > 1
    assert len(db_sla.projects) > 1
    return db_sla


db_sla = fixture_union(
    "db_sla", (db_sla_simple, db_sla_with_multiple_projects), idstyle="explicit"
)
