"""SLA specific fixtures."""

from typing import Any, Dict

from pytest_cases import fixture, fixture_union

from app.identity_provider.crud import identity_provider_mng
from app.identity_provider.models import IdentityProvider
from app.provider.models import Provider
from app.provider.schemas_extended import (
    AuthMethodCreate,
    IdentityProviderCreateExtended,
    SLACreateExtended,
    UserGroupCreateExtended,
)
from app.sla.models import SLA
from app.user_group.models import UserGroup
from tests.common.utils import random_lower_string


@fixture
def db_sla_simple(db_user_group_simple: UserGroup) -> SLA:
    """Fixture with standard DB SLA."""
    return db_user_group_simple.slas.single()


@fixture
def db_sla_with_multiple_projects(
    identity_provider_create_mandatory_data: Dict[str, Any],
    sla_create_mandatory_data: Dict[str, Any],
    db_provider_with_single_project: Provider,
    db_provider_with_projects: Provider,
) -> IdentityProvider:
    """IdentityProvider shared within multiple providers."""
    name = random_lower_string()
    sla = SLACreateExtended(
        **sla_create_mandatory_data,
        project=db_provider_with_single_project.projects.single().uuid,
    )
    item = IdentityProviderCreateExtended(
        **identity_provider_create_mandatory_data,
        relationship=AuthMethodCreate(
            idp_name=random_lower_string(), protocol=random_lower_string()
        ),
        user_groups=[UserGroupCreateExtended(name=name, sla=sla)],
    )
    db_idp = identity_provider_mng.create(
        obj_in=item, provider=db_provider_with_single_project
    )

    sla.project = db_provider_with_projects.projects.single().uuid
    item = IdentityProviderCreateExtended(
        **identity_provider_create_mandatory_data,
        relationship=AuthMethodCreate(
            idp_name=random_lower_string(), protocol=random_lower_string()
        ),
        user_groups=[UserGroupCreateExtended(name=name, sla=sla)],
    )
    db_idp = identity_provider_mng.create(
        obj_in=item, provider=db_provider_with_projects
    )

    db_user_group: UserGroup = db_idp.user_groups.single()
    db_sla: SLA = db_user_group.slas.single()
    assert len(db_idp.providers) > 1
    assert len(db_sla.projects) > 1
    return db_sla


db_sla = fixture_union(
    "db_sla", (db_sla_simple, db_sla_with_multiple_projects), idstyle="explicit"
)
