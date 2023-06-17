from typing import List, Optional, Tuple

from .. import schemas, models


def connect_sla_to_user_group(
    item: models.Provider, user_group: models.UserGroup
) -> None:
    if not item.user_group.is_connected(user_group):
        item.user_group.connect(user_group)


def connect_sla_to_project(
    item: models.Provider, project: models.Project
) -> None:
    if not item.project.is_connected(project):
        item.project.connect(project)


def connect_sla_to_services(
    sla: models.SLA,
    services: List[Tuple[models.Service, List[schemas.QuotaCreate]]],
) -> None:
    for service, quotas in services:
        for quota in quotas:
            sla.services.connect(service, quota.dict())


def create_sla(
    item: schemas.SLACreate,
    project: models.Project,
    user_group: models.UserGroup,
    services: List[Tuple[models.Service, List[schemas.QuotaCreate]]],
) -> models.SLA:
    db_item = models.SLA(
        **item.dict(exclude={"project", "services", "user_group"})
    ).save()
    connect_sla_to_project(db_item, project)
    connect_sla_to_user_group(db_item, user_group)
    connect_sla_to_services(db_item, services)
    return db_item


def get_slas(
    skip: int = 0,
    limit: Optional[int] = None,
    sort: Optional[str] = None,
    **kwargs,
) -> List[models.SLA]:
    if kwargs:
        items = models.SLA.nodes.filter(**kwargs).order_by(sort).all()
    else:
        items = models.SLA.nodes.order_by(sort).all()
    if limit is None:
        return items[skip:]
    return items[skip : skip + limit]


def get_sla(**kwargs) -> Optional[models.SLA]:
    return models.SLA.nodes.get_or_none(**kwargs)


def remove_sla(item: models.SLA) -> bool:
    return item.delete()


# TODO
def update_sla(
    old_item: models.SLA, new_item: schemas.SLAUpdate
) -> Optional[models.SLA]:
    for k, v in new_item.dict(
        exclude={"project", "services", "user_group"},
        exclude_unset=True,
    ).items():
        old_item.__setattr__(k, v)
    if new_item.project is not None:
        connect_sla_to_project(old_item, new_item.project)
    if new_item.user_group is not None:
        connect_sla_to_user_group(old_item, new_item.user_group)
    if len(new_item.services) > 0:
        connect_sla_to_services(old_item, new_item.services)
    old_item.save()
    return old_item
