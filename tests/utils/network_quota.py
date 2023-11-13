from typing import Union

from app.provider.schemas_extended import NetworkQuotaCreateExtended
from app.quota.models import NetworkQuota
from app.quota.schemas import (
    NetworkQuotaBase,
    NetworkQuotaRead,
    NetworkQuotaReadPublic,
    NetworkQuotaReadShort,
    NetworkQuotaUpdate,
)
from app.quota.schemas_extended import (
    NetworkQuotaReadExtended,
    NetworkQuotaReadExtendedPublic,
)
from tests.utils.utils import (
    random_bool,
    random_lower_string,
    random_non_negative_int,
)


def create_random_network_quota(
    *, default: bool = False, project: str
) -> NetworkQuotaCreateExtended:
    kwargs = {}
    if not default:
        kwargs = {
            "description": random_lower_string(),
            "per_user": random_bool(),
            "public_ips": random_non_negative_int(),
            "networks": random_non_negative_int(),
            "ports": random_non_negative_int(),
            "security_groups": random_non_negative_int(),
            "security_group_rules": random_non_negative_int(),
        }
    return NetworkQuotaCreateExtended(project=project, **kwargs)


def create_random_network_quota_patch(
    default: bool = False,
) -> NetworkQuotaUpdate:
    if default:
        return NetworkQuotaUpdate()
    description = random_lower_string()
    per_user = random_bool()
    public_ips = random_non_negative_int()
    networks = random_non_negative_int()
    ports = random_non_negative_int()
    security_groups = random_non_negative_int()
    security_group_rules = random_non_negative_int()
    return NetworkQuotaUpdate(
        description=description,
        per_user=per_user,
        public_ips=public_ips,
        networks=networks,
        ports=ports,
        security_groups=security_groups,
        security_group_rules=security_group_rules,
    )


def validate_public_attrs(*, obj_in: NetworkQuotaBase, db_item: NetworkQuota) -> None:
    assert db_item.description == obj_in.description
    assert db_item.type == obj_in.type
    assert db_item.per_user == obj_in.per_user
    assert db_item.public_ips == obj_in.public_ips
    assert db_item.networks == obj_in.networks
    assert db_item.ports == obj_in.ports
    assert db_item.security_groups == obj_in.security_groups
    assert db_item.security_group_rules == obj_in.security_group_rules


def validate_attrs(*, obj_in: NetworkQuotaBase, db_item: NetworkQuota) -> None:
    validate_public_attrs(obj_in=obj_in, db_item=db_item)


def validate_rels(
    *,
    obj_out: Union[NetworkQuotaReadExtended, NetworkQuotaReadExtendedPublic],
    db_item: NetworkQuota,
) -> None:
    db_project = db_item.project.single()
    assert db_project
    assert db_project.uid == obj_out.project.uid
    db_service = db_item.service.single()
    assert db_service
    assert db_service.uid == obj_out.service.uid


def validate_create_network_quota_attrs(
    *, obj_in: NetworkQuotaCreateExtended, db_item: NetworkQuota
) -> None:
    validate_attrs(obj_in=obj_in, db_item=db_item)
    db_project = db_item.project.single()
    assert db_project
    assert db_project.uuid == obj_in.project


def validate_read_network_quota_attrs(
    *, obj_out: NetworkQuotaRead, db_item: NetworkQuota
) -> None:
    assert db_item.uid == obj_out.uid
    validate_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_short_network_quota_attrs(
    *, obj_out: NetworkQuotaReadShort, db_item: NetworkQuota
) -> None:
    assert db_item.uid == obj_out.uid
    validate_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_public_network_quota_attrs(
    *, obj_out: NetworkQuotaReadPublic, db_item: NetworkQuota
) -> None:
    assert db_item.uid == obj_out.uid
    validate_public_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_extended_network_quota_attrs(
    *, obj_out: NetworkQuotaReadExtended, db_item: NetworkQuota
) -> None:
    assert db_item.uid == obj_out.uid
    validate_attrs(obj_in=obj_out, db_item=db_item)
    validate_rels(obj_out=obj_out, db_item=db_item)


def validate_read_extended_public_network_quota_attrs(
    *, obj_out: NetworkQuotaReadExtendedPublic, db_item: NetworkQuota
) -> None:
    assert db_item.uid == obj_out.uid
    validate_public_attrs(obj_in=obj_out, db_item=db_item)
    validate_rels(obj_out=obj_out, db_item=db_item)
