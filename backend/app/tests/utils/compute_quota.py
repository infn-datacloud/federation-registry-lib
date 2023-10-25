from app.provider.schemas_extended import ComputeQuotaCreateExtended
from app.quota.models import ComputeQuota
from app.quota.schemas import (
    ComputeQuotaBase,
    ComputeQuotaRead,
    ComputeQuotaReadPublic,
    ComputeQuotaReadShort,
    ComputeQuotaUpdate,
)
from app.quota.schemas_extended import (
    ComputeQuotaReadExtended,
    ComputeQuotaReadExtendedPublic,
)
from app.tests.utils.utils import (
    random_bool,
    random_lower_string,
    random_non_negative_int,
)


def create_random_compute_quota(
    *, default: bool = False, project: str
) -> ComputeQuotaCreateExtended:
    kwargs = {}
    if not default:
        kwargs = {
            "description": random_lower_string(),
            "per_user": random_bool(),
            "cores": random_non_negative_int(),
            "fixed_ips": random_non_negative_int(),
            "public_ips": random_non_negative_int(),
            "instances": random_non_negative_int(),
            "ram": random_non_negative_int(),
        }
    return ComputeQuotaCreateExtended(project=project, **kwargs)


def create_random_compute_quota_patch(default: bool = False) -> ComputeQuotaUpdate:
    if default:
        return ComputeQuotaUpdate()
    description = random_lower_string()
    per_user = random_bool()
    cores = random_non_negative_int()
    fixed_ips = random_non_negative_int()
    public_ips = random_non_negative_int()
    instances = random_non_negative_int()
    ram = random_non_negative_int()
    return ComputeQuotaUpdate(
        description=description,
        per_user=per_user,
        cores=cores,
        fixed_ips=fixed_ips,
        public_ips=public_ips,
        instances=instances,
        ram=ram,
    )


def validate_compute_quota_attrs(
    *, obj_in: ComputeQuotaBase, db_item: ComputeQuota
) -> None:
    assert db_item.description == obj_in.description
    assert db_item.type == obj_in.type
    assert db_item.per_user == obj_in.per_user
    assert db_item.cores == obj_in.cores
    assert db_item.fixed_ips == obj_in.fixed_ips
    assert db_item.public_ips == obj_in.public_ips
    assert db_item.instances == obj_in.instances
    assert db_item.ram == obj_in.ram


def validate_compute_quota_public_attrs(
    *, obj_in: ComputeQuotaBase, db_item: ComputeQuota
) -> None:
    assert db_item.description == obj_in.description
    assert db_item.type == obj_in.type
    assert db_item.per_user == obj_in.per_user
    assert db_item.cores == obj_in.cores
    assert db_item.fixed_ips == obj_in.fixed_ips
    assert db_item.public_ips == obj_in.public_ips
    assert db_item.instances == obj_in.instances
    assert db_item.ram == obj_in.ram


def validate_create_compute_quota_attrs(
    *, obj_in: ComputeQuotaCreateExtended, db_item: ComputeQuota
) -> None:
    validate_compute_quota_attrs(obj_in=obj_in, db_item=db_item)
    db_project = db_item.project.single()
    assert db_project
    assert db_project.uuid == obj_in.project


def validate_read_compute_quota_attrs(
    *, obj_out: ComputeQuotaRead, db_item: ComputeQuota
) -> None:
    assert db_item.uid == obj_out.uid
    validate_compute_quota_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_short_compute_quota_attrs(
    *, obj_out: ComputeQuotaReadShort, db_item: ComputeQuota
) -> None:
    assert db_item.uid == obj_out.uid
    validate_compute_quota_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_public_compute_quota_attrs(
    *, obj_out: ComputeQuotaReadPublic, db_item: ComputeQuota
) -> None:
    assert db_item.uid == obj_out.uid
    validate_compute_quota_public_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_extended_compute_quota_attrs(
    *, obj_out: ComputeQuotaReadExtended, db_item: ComputeQuota
) -> None:
    assert db_item.uid == obj_out.uid
    validate_compute_quota_attrs(obj_in=obj_out, db_item=db_item)
    db_project = db_item.project.single()
    assert db_project
    assert db_project.uid == obj_out.project.uid
    db_service = db_item.service.single()
    assert db_service
    assert db_service.uid == obj_out.service.uid


def validate_read_extended_public_compute_quota_attrs(
    *, obj_out: ComputeQuotaReadExtendedPublic, db_item: ComputeQuota
) -> None:
    assert db_item.uid == obj_out.uid
    validate_compute_quota_public_attrs(obj_in=obj_out, db_item=db_item)
    db_project = db_item.project.single()
    assert db_project
    assert db_project.uid == obj_out.project.uid
    db_service = db_item.service.single()
    assert db_service
    assert db_service.uid == obj_out.service.uid
