from random import choice
from typing import List, Union

from app.provider.schemas_extended import BlockStorageServiceCreateExtended
from app.service.enum import BlockStorageServiceName
from app.service.models import BlockStorageService
from app.service.schemas import (
    BlockStorageServiceBase,
    BlockStorageServiceRead,
    BlockStorageServiceReadPublic,
    BlockStorageServiceReadShort,
    BlockStorageServiceUpdate,
)
from app.service.schemas_extended import (
    BlockStorageServiceReadExtended,
    BlockStorageServiceReadExtendedPublic,
)
from tests.utils.block_storage_quota import (
    create_random_block_storage_quota,
    validate_create_block_storage_quota_attrs,
)
from tests.utils.utils import random_lower_string, random_url


def create_random_block_storage_service(
    *, default: bool = False, projects: List[str] = []
) -> BlockStorageServiceCreateExtended:
    endpoint = random_url()
    name = random_block_storage_service_name()
    kwargs = {}
    if not default:
        kwargs = {"description": random_lower_string()}
    if len(projects):
        kwargs["quotas"] = [create_random_block_storage_quota(project=projects[0])]
    return BlockStorageServiceCreateExtended(endpoint=endpoint, name=name, **kwargs)


def create_random_block_storage_service_patch(
    default: bool = False,
) -> BlockStorageServiceUpdate:
    if default:
        return BlockStorageServiceUpdate()
    description = random_lower_string()
    endpoint = random_url()
    name = random_block_storage_service_name()
    return BlockStorageServiceUpdate(
        description=description, endpoint=endpoint, name=name
    )


def random_block_storage_service_name() -> str:
    return choice([i.value for i in BlockStorageServiceName])


def validate_public_attrs(
    *, obj_in: BlockStorageServiceBase, db_item: BlockStorageService
) -> None:
    assert db_item.description == obj_in.description
    assert db_item.endpoint == obj_in.endpoint
    assert db_item.name == obj_in.name
    assert db_item.type == obj_in.type


def validate_attrs(
    *, obj_in: BlockStorageServiceBase, db_item: BlockStorageService
) -> None:
    validate_public_attrs(obj_in=obj_in, db_item=db_item)


def validate_rels(
    *,
    obj_out: Union[
        BlockStorageServiceReadExtended, BlockStorageServiceReadExtendedPublic
    ],
    db_item: BlockStorageService
) -> None:
    db_region = db_item.region.single()
    assert db_region
    assert db_region.uid == obj_out.region.uid
    assert len(db_item.quotas) == len(obj_out.quotas)
    for db_quota, quota_out in zip(
        sorted(db_item.quotas, key=lambda x: x.uid),
        sorted(obj_out.quotas, key=lambda x: x.uid),
    ):
        assert db_quota.uid == quota_out.uid


def validate_create_block_storage_service_attrs(
    *, obj_in: BlockStorageServiceCreateExtended, db_item: BlockStorageService
) -> None:
    validate_attrs(obj_in=obj_in, db_item=db_item)
    assert len(db_item.quotas) == len(obj_in.quotas)
    for db_quota, quota_in in zip(
        sorted(db_item.quotas, key=lambda x: x.description),
        sorted(obj_in.quotas, key=lambda x: x.description),
    ):
        validate_create_block_storage_quota_attrs(db_item=db_quota, obj_in=quota_in)


def validate_read_block_storage_service_attrs(
    *, obj_out: BlockStorageServiceRead, db_item: BlockStorageService
) -> None:
    assert db_item.uid == obj_out.uid
    validate_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_short_block_storage_service_attrs(
    *, obj_out: BlockStorageServiceReadShort, db_item: BlockStorageService
) -> None:
    assert db_item.uid == obj_out.uid
    validate_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_public_block_storage_service_attrs(
    *, obj_out: BlockStorageServiceReadPublic, db_item: BlockStorageService
) -> None:
    assert db_item.uid == obj_out.uid
    validate_public_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_extended_block_storage_service_attrs(
    *, obj_out: BlockStorageServiceReadExtended, db_item: BlockStorageService
) -> None:
    assert db_item.uid == obj_out.uid
    validate_attrs(obj_in=obj_out, db_item=db_item)
    validate_rels(obj_out=obj_out, db_item=db_item)


def validate_read_extended_public_block_storage_service_attrs(
    *, obj_out: BlockStorageServiceReadExtendedPublic, db_item: BlockStorageService
) -> None:
    assert db_item.uid == obj_out.uid
    validate_public_attrs(obj_in=obj_out, db_item=db_item)
    validate_rels(obj_out=obj_out, db_item=db_item)
