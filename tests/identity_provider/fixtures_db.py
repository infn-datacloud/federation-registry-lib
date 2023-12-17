"""IdentityProvider specific fixtures."""
from uuid import uuid4

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
from tests.common.utils import random_lower_string
from tests.identity_provider.utils import random_identity_provider_required_attr
from tests.sla.utils import random_start_end_dates


@fixture
def db_identity_provider_simple(
    db_provider_with_single_project: Provider,
) -> IdentityProvider:
    """Fixture with standard DB IdentityProvider."""
    start_date, end_date = random_start_end_dates()
    item = IdentityProviderCreateExtended(
        **random_identity_provider_required_attr(),
        relationship=AuthMethodCreate(
            idp_name=random_lower_string(), protocol=random_lower_string()
        ),
        user_groups=[
            UserGroupCreateExtended(
                name=random_lower_string(),
                sla=SLACreateExtended(
                    doc_uuid=uuid4(),
                    start_date=start_date,
                    end_date=end_date,
                    project=db_provider_with_single_project.projects.single().uuid,
                ),
            )
        ],
    )
    return identity_provider_mng.create(
        obj_in=item, provider=db_provider_with_single_project
    )


@fixture
def db_shared_identity_provider(
    db_provider_with_single_project: Provider,
    db_provider_with_projects: Provider,
) -> IdentityProvider:
    """IdentityProvider shared within multiple providers."""
    idp_data = random_identity_provider_required_attr()
    name = random_lower_string()
    start_date, end_date = random_start_end_dates()
    sla = SLACreateExtended(
        doc_uuid=uuid4(),
        start_date=start_date,
        end_date=end_date,
        project=db_provider_with_single_project.projects.single().uuid,
    )
    item = IdentityProviderCreateExtended(
        **idp_data,
        relationship=AuthMethodCreate(
            idp_name=random_lower_string(), protocol=random_lower_string()
        ),
        user_groups=[UserGroupCreateExtended(name=name, sla=sla)],
    )
    db_item = identity_provider_mng.create(
        obj_in=item, provider=db_provider_with_single_project
    )

    sla = SLACreateExtended(
        doc_uuid=uuid4(),
        start_date=start_date,
        end_date=end_date,
        project=db_provider_with_projects.projects.single().uuid,
    )
    item = IdentityProviderCreateExtended(
        **idp_data,
        relationship=AuthMethodCreate(
            idp_name=random_lower_string(), protocol=random_lower_string()
        ),
        user_groups=[UserGroupCreateExtended(name=name, sla=sla)],
    )
    db_item = identity_provider_mng.create(
        obj_in=item, provider=db_provider_with_projects
    )

    assert len(db_item.providers) > 1
    return db_item


db_identity_provider = fixture_union(
    "db_identity_provider",
    (db_identity_provider_simple, db_shared_identity_provider),
    idstyle="explicit",
)
