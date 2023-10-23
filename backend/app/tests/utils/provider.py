from random import choice

from app.provider.enum import ProviderStatus, ProviderType
from app.provider.models import Provider
from app.provider.schemas import ProviderUpdate
from app.provider.schemas_extended import ProviderCreateExtended
from app.tests.utils.identity_provider import (
    create_random_identity_provider,
    validate_identity_provider_attrs,
)
from app.tests.utils.project import create_random_project, validate_project_attrs
from app.tests.utils.region import create_random_region, validate_region_attrs
from app.tests.utils.utils import random_bool, random_email, random_lower_string


def create_random_provider(
    *,
    default: bool = False,
    with_identity_providers: bool = False,
    with_projects: bool = False,
    with_regions: bool = False,
) -> ProviderCreateExtended:
    name = random_lower_string()
    type = random_type()
    kwargs = {}
    if not default:
        kwargs = {
            "description": random_lower_string(),
            "is_public": random_bool(),
            "support_emails": [random_email()],
            "status": random_status(),
        }
    if with_projects:
        kwargs["projects"] = [create_random_project()]
    projects = [i.uuid for i in kwargs.get("projects", [])]
    if with_identity_providers:
        kwargs["identity_providers"] = [
            create_random_identity_provider(projects=projects)
        ]
    if with_regions:
        kwargs["regions"] = [
            create_random_region(
                with_location=True,
                with_block_storage_services=True,
                with_compute_services=True,
                with_identity_services=True,
                with_network_services=True,
                projects=projects,
            )
        ]
    return ProviderCreateExtended(name=name, type=type, **kwargs)


def create_random_provider_patch(*, default: bool = False) -> ProviderUpdate:
    if default:
        return ProviderUpdate()
    description = random_lower_string()
    name = random_lower_string()
    type = random_type()
    is_public = random_bool()
    support_emails = [random_email()]
    status = random_status()
    return ProviderUpdate(
        description=description,
        name=name,
        type=type,
        is_public=is_public,
        support_emails=support_emails,
        status=status,
    )


def random_status() -> str:
    return choice([i.value for i in ProviderStatus])


def random_type() -> str:
    return choice([i.value for i in ProviderType])


def validate_provider_attrs(
    *, obj_in: ProviderCreateExtended, db_item: Provider
) -> None:
    assert obj_in
    assert db_item
    assert db_item.description == obj_in.description
    assert db_item.name == obj_in.name
    assert db_item.type == obj_in.type
    assert db_item.is_public == obj_in.is_public
    assert db_item.status == obj_in.status
    assert db_item.support_emails == obj_in.support_emails
    assert len(db_item.projects) == len(obj_in.projects)
    for db_proj, proj_in in zip(db_item.projects, obj_in.projects):
        validate_project_attrs(obj_in=proj_in, db_item=db_proj)
    assert len(db_item.identity_providers) == len(obj_in.identity_providers)
    for db_idp, idp_in in zip(db_item.identity_providers, obj_in.identity_providers):
        validate_identity_provider_attrs(obj_in=idp_in, db_item=db_idp)
    assert len(db_item.regions) == len(obj_in.regions)
    for db_reg, reg_in in zip(db_item.regions, obj_in.regions):
        validate_region_attrs(obj_in=reg_in, db_item=db_reg)
