from random import choice
from typing import Union

from app.service.enum import IdentityServiceName
from app.service.models import IdentityService
from app.service.schemas import (
    IdentityServiceBase,
    IdentityServiceCreate,
    IdentityServiceRead,
    IdentityServiceReadPublic,
    IdentityServiceReadShort,
    IdentityServiceUpdate,
)
from app.service.schemas_extended import (
    IdentityServiceReadExtended,
    IdentityServiceReadExtendedPublic,
)
from tests.utils.utils import random_lower_string, random_url


def create_random_identity_service(*, default: bool = False) -> IdentityServiceCreate:
    endpoint = random_url()
    name = random_identity_service_name()
    kwargs = {}
    if not default:
        kwargs = {"description": random_lower_string()}
    return IdentityServiceCreate(endpoint=endpoint, name=name, **kwargs)


def create_random_identity_service_patch(
    default: bool = False,
) -> IdentityServiceUpdate:
    if default:
        return IdentityServiceUpdate()
    description = random_lower_string()
    endpoint = random_url()
    name = random_identity_service_name()
    return IdentityServiceUpdate(description=description, endpoint=endpoint, name=name)


def random_identity_service_name() -> str:
    return choice([i.value for i in IdentityServiceName])


def validate_public_attrs(
    *, obj_in: IdentityServiceBase, db_item: IdentityService
) -> None:
    assert db_item.description == obj_in.description
    assert db_item.endpoint == obj_in.endpoint
    assert db_item.name == obj_in.name
    assert db_item.type == obj_in.type


def validate_attrs(*, obj_in: IdentityServiceBase, db_item: IdentityService) -> None:
    validate_public_attrs(obj_in=obj_in, db_item=db_item)


def validate_rels(
    *,
    obj_out: Union[IdentityServiceReadExtended, IdentityServiceReadExtendedPublic],
    db_item: IdentityService
):
    db_region = db_item.region.single()
    assert db_region
    assert db_region.uid == obj_out.region.uid


def validate_create_identity_service_attrs(
    *, obj_in: IdentityServiceCreate, db_item: IdentityService
) -> None:
    validate_attrs(obj_in=obj_in, db_item=db_item)


def validate_read_identity_service_attrs(
    *, obj_out: IdentityServiceRead, db_item: IdentityService
) -> None:
    assert db_item.uid == obj_out.uid
    validate_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_short_identity_service_attrs(
    *, obj_out: IdentityServiceReadShort, db_item: IdentityService
) -> None:
    assert db_item.uid == obj_out.uid
    validate_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_public_identity_service_attrs(
    *, obj_out: IdentityServiceReadPublic, db_item: IdentityService
) -> None:
    assert db_item.uid == obj_out.uid
    validate_public_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_extended_identity_service_attrs(
    *, obj_out: IdentityServiceReadExtended, db_item: IdentityService
) -> None:
    assert db_item.uid == obj_out.uid
    validate_attrs(obj_in=obj_out, db_item=db_item)
    validate_rels(obj_out=obj_out, db_item=db_item)


def validate_read_extended_public_identity_service_attrs(
    *, obj_out: IdentityServiceReadExtendedPublic, db_item: IdentityService
) -> None:
    assert db_item.uid == obj_out.uid
    validate_public_attrs(obj_in=obj_out, db_item=db_item)
    validate_rels(obj_out=obj_out, db_item=db_item)
