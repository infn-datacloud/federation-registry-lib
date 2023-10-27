from random import choice

from app.provider.enum import ProviderStatus, ProviderType
from app.provider.models import Provider
from app.provider.schemas import (
    ProviderBase,
    ProviderRead,
    ProviderReadPublic,
    ProviderReadShort,
    ProviderUpdate,
)
from app.provider.schemas_extended import (
    ProviderCreateExtended,
    ProviderReadExtended,
    ProviderReadExtendedPublic,
)
from tests.utils.identity_provider import (
    create_random_identity_provider,
    validate_create_identity_provider_attrs,
)
from tests.utils.project import create_random_project, validate_create_project_attrs
from tests.utils.region import create_random_region, validate_create_region_attrs
from tests.utils.utils import random_bool, random_email, random_lower_string


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


def validate_provider_attrs(*, obj_in: ProviderBase, db_item: Provider) -> None:
    assert obj_in
    assert db_item
    assert db_item.description == obj_in.description
    assert db_item.name == obj_in.name
    assert db_item.type == obj_in.type
    assert db_item.is_public == obj_in.is_public
    assert db_item.status == obj_in.status
    assert db_item.support_emails == obj_in.support_emails


def validate_provider_public_attrs(*, obj_in: ProviderBase, db_item: Provider) -> None:
    assert obj_in
    assert db_item
    assert db_item.description == obj_in.description
    assert db_item.name == obj_in.name
    assert db_item.type == obj_in.type
    assert db_item.is_public == obj_in.is_public
    assert db_item.status == obj_in.status
    assert db_item.support_emails == obj_in.support_emails


def validate_create_provider_attrs(
    *, obj_in: ProviderCreateExtended, db_item: Provider
) -> None:
    validate_provider_attrs(obj_in=obj_in, db_item=db_item)
    assert len(db_item.projects) == len(obj_in.projects)
    for db_proj, proj_in in zip(db_item.projects, obj_in.projects):
        validate_create_project_attrs(obj_in=proj_in, db_item=db_proj)
    assert len(db_item.identity_providers) == len(obj_in.identity_providers)
    for db_idp, idp_in in zip(db_item.identity_providers, obj_in.identity_providers):
        validate_create_identity_provider_attrs(obj_in=idp_in, db_item=db_idp)
    assert len(db_item.regions) == len(obj_in.regions)
    for db_reg, reg_in in zip(db_item.regions, obj_in.regions):
        validate_create_region_attrs(obj_in=reg_in, db_item=db_reg)


def validate_read_provider_attrs(*, obj_out: ProviderRead, db_item: Provider) -> None:
    assert db_item.uid == obj_out.uid
    validate_provider_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_short_provider_attrs(
    *, obj_out: ProviderReadShort, db_item: Provider
) -> None:
    assert db_item.uid == obj_out.uid
    validate_provider_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_public_provider_attrs(
    *, obj_out: ProviderReadPublic, db_item: Provider
) -> None:
    assert db_item.uid == obj_out.uid
    validate_provider_public_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_extended_provider_attrs(
    *, obj_out: ProviderReadExtended, db_item: Provider
) -> None:
    assert db_item.uid == obj_out.uid
    validate_provider_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_extended_public_provider_attrs(
    *, obj_out: ProviderReadExtendedPublic, db_item: Provider
) -> None:
    assert db_item.uid == obj_out.uid
    validate_provider_public_attrs(obj_in=obj_out, db_item=db_item)
    assert len(db_item.projects) == len(obj_out.projects)
    for db_proj, proj_out in zip(db_item.projects, obj_out.projects):
        assert db_proj.uid == proj_out.uid
    assert len(db_item.identity_providers) == len(obj_out.identity_providers)
    for db_idp, idp_out in zip(db_item.identity_providers, obj_out.identity_providers):
        assert db_idp.uid == idp_out.uid
    assert len(db_item.regions) == len(obj_out.regions)
    for db_reg, reg_out in zip(db_item.regions, obj_out.regions):
        assert db_reg.uid == reg_out.uid
