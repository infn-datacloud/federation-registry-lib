from typing import List, Optional
from .. import schemas, models


def create_sla(item: schemas.SLACreate) -> schemas.SLA:
    return models.SLA(**item.dict()).save()


def get_slas(**kwargs) -> List[schemas.SLA]:
    if kwargs:
        return models.SLA.nodes.filter(**kwargs).all()
    return models.SLA.nodes.all()


def get_sla(**kwargs) -> Optional[schemas.SLA]:
    return models.SLA.nodes.get_or_none(**kwargs)


def remove_sla(item: models.SLA) -> bool:
    return item.delete()


def connect_sla_to_project_and_provider(
    project: models.Project, provider: models.Provider, sla: models.SLA
) -> bool:
    return sla.project.connect(project) and sla.provider.connect(provider)
