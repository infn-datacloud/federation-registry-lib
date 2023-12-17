"""SLA specific fixtures."""
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
from tests.identity_provider.utils import (
    random_identity_provider_required_attr,
)
from tests.sla.utils import random_sla_required_attr


@fixture
def db_sla_simple(db_user_group_simple: UserGroup) -> SLA:
    """Fixture with standard DB SLA."""
    return db_user_group_simple.slas.single()


@fixture
def db_sla_with_multiple_projects(
    db_provider_with_single_project: Provider,
    db_provider_with_projects: Provider,
) -> IdentityProvider:
    """IdentityProvider shared within multiple providers."""
    sla = SLACreateExtended(
        **random_sla_required_attr(),
        project=db_provider_with_single_project.projects.single().uuid,
    )
    item = IdentityProviderCreateExtended(
        **random_identity_provider_required_attr(),
        relationship=AuthMethodCreate(
            idp_name=random_lower_string(), protocol=random_lower_string()
        ),
        user_groups=[UserGroupCreateExtended(name=random_lower_string(), sla=sla)],
    )
    db_idp = identity_provider_mng.create(
        obj_in=item, provider=db_provider_with_single_project
    )

    item.user_groups[0].sla.project = db_provider_with_projects.projects.single().uuid
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
