from typing import List, Optional
from .. import schemas, models


def create_quota(item: schemas.QuotaCreate) -> schemas.Quota:
    return models.Quota(**item.dict()).save()


def get_quotas(**kwargs) -> List[schemas.Quota]:
    if kwargs:
        return models.Quota.nodes.filter(**kwargs).all()
    return models.Quota.nodes.all()


def get_quota(**kwargs) -> Optional[schemas.Quota]:
    return models.Quota.nodes.get_or_none(**kwargs)


def remove_quota(item: models.Quota) -> bool:
    return item.delete()


def connect_quota_to_sla(sla: models.SLA, quota: models.Quota) -> bool:
    return quota.sla.connect(sla)
