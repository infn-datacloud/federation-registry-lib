from random import choice
from typing import List

from app.provider.schemas_extended import ComputeServiceCreateExtended
from app.service.enum import ComputeServiceName
from app.service.models import ComputeService
from app.service.schemas import (
    ComputeServiceBase,
    ComputeServiceRead,
    ComputeServiceReadPublic,
    ComputeServiceReadShort,
    ComputeServiceUpdate,
)
from app.service.schemas_extended import (
    ComputeServiceReadExtended,
    ComputeServiceReadExtendedPublic,
)
from tests.utils.compute_quota import (
    create_random_compute_quota,
    validate_create_compute_quota_attrs,
)
from tests.utils.flavor import create_random_flavor, validate_create_flavor_attrs
from tests.utils.image import create_random_image, validate_create_image_attrs
from tests.utils.utils import random_lower_string, random_url


def create_random_compute_service(
    *,
    default: bool = False,
    with_flavors: bool = False,
    with_images: bool = False,
    projects: List[str] = [],
) -> ComputeServiceCreateExtended:
    endpoint = random_url()
    name = random_compute_service_name()
    kwargs = {}
    if not default:
        kwargs = {"description": random_lower_string()}
    if with_flavors:
        kwargs["flavors"] = [create_random_flavor(projects=projects)]
    if with_images:
        kwargs["images"] = [create_random_image(projects=projects)]
    if len(projects):
        kwargs["quotas"] = [create_random_compute_quota(project=projects[0])]
    return ComputeServiceCreateExtended(endpoint=endpoint, name=name, **kwargs)


def create_random_compute_service_patch(
    default: bool = False,
) -> ComputeServiceUpdate:
    if default:
        return ComputeServiceUpdate()
    description = random_lower_string()
    endpoint = random_url()
    name = random_compute_service_name()
    return ComputeServiceUpdate(description=description, endpoint=endpoint, name=name)


def random_compute_service_name() -> str:
    return choice([i.value for i in ComputeServiceName])


def validate_compute_service_attrs(
    *, obj_in: ComputeServiceBase, db_item: ComputeService
) -> None:
    assert db_item.description == obj_in.description
    assert db_item.endpoint == obj_in.endpoint
    assert db_item.name == obj_in.name
    assert db_item.type == obj_in.type


def validate_compute_service_public_attrs(
    *, obj_in: ComputeServiceBase, db_item: ComputeService
) -> None:
    assert db_item.description == obj_in.description
    assert db_item.endpoint == obj_in.endpoint
    assert db_item.name == obj_in.name
    assert db_item.type == obj_in.type


def validate_create_compute_service_attrs(
    *, obj_in: ComputeServiceCreateExtended, db_item: ComputeService
) -> None:
    validate_compute_service_attrs(obj_in=obj_in, db_item=db_item)
    assert len(db_item.quotas) == len(obj_in.quotas)
    for db_quota, quota_in in zip(db_item.quotas, obj_in.quotas):
        validate_create_compute_quota_attrs(db_item=db_quota, obj_in=quota_in)


def validate_read_compute_service_attrs(
    *, obj_out: ComputeServiceRead, db_item: ComputeService
) -> None:
    assert db_item.uid == obj_out.uid
    validate_compute_service_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_short_compute_service_attrs(
    *, obj_out: ComputeServiceReadShort, db_item: ComputeService
) -> None:
    assert db_item.uid == obj_out.uid
    validate_compute_service_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_public_compute_service_attrs(
    *, obj_out: ComputeServiceReadPublic, db_item: ComputeService
) -> None:
    assert db_item.uid == obj_out.uid
    validate_compute_service_public_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_extended_compute_service_attrs(
    *, obj_out: ComputeServiceReadExtended, db_item: ComputeService
) -> None:
    assert db_item.uid == obj_out.uid
    validate_compute_service_attrs(obj_in=obj_out, db_item=db_item)
    assert len(db_item.flavors) == len(obj_out.flavors)
    for db_flav, flav_in in zip(db_item.flavors, obj_out.flavors):
        validate_create_flavor_attrs(db_item=db_flav, obj_out=flav_in)
    assert len(db_item.images) == len(obj_out.images)
    for db_img, img_in in zip(db_item.images, obj_out.images):
        validate_create_image_attrs(db_item=db_img, obj_out=img_in)
    assert len(db_item.quotas) == len(obj_out.quotas)
    for db_quota, quota_in in zip(db_item.quotas, obj_out.quotas):
        validate_create_compute_quota_attrs(db_item=db_quota, obj_out=quota_in)
    db_region = db_item.region.single()
    assert db_region
    assert db_region.uid == obj_out.region.uid


def validate_read_extended_public_compute_service_attrs(
    *, obj_out: ComputeServiceReadExtendedPublic, db_item: ComputeService
) -> None:
    assert db_item.uid == obj_out.uid
    validate_compute_service_public_attrs(obj_in=obj_out, db_item=db_item)
    assert len(db_item.flavors) == len(obj_out.flavors)
    for db_flav, flav_in in zip(db_item.flavors, obj_out.flavors):
        validate_create_flavor_attrs(db_item=db_flav, obj_out=flav_in)
    assert len(db_item.images) == len(obj_out.images)
    for db_img, img_in in zip(db_item.images, obj_out.images):
        validate_create_image_attrs(db_item=db_img, obj_out=img_in)
    assert len(db_item.quotas) == len(obj_out.quotas)
    for db_quota, quota_in in zip(db_item.quotas, obj_out.quotas):
        validate_create_compute_quota_attrs(db_item=db_quota, obj_out=quota_in)
    db_region = db_item.region.single()
    assert db_region
    assert db_region.uid == obj_out.region.uid
