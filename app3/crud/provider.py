from typing import List, Optional

from .cluster import create_cluster, read_cluster
from .flavor import create_flavor, read_flavor
from .identity_provider import create_identity_provider, read_identity_provider
from .image import create_image, read_image
from .location import create_location, read_location
from .project import create_project, read_project
from .service import create_service, read_service
from .utils import truncate
from .. import schemas, models


def connect_provider_to_idps(
    item: models.Provider,
    identity_providers: List[schemas.IdentityProviderCreateExtended],
) -> None:
    for identity_provider in identity_providers:
        db_idp = read_identity_provider(
            **identity_provider.dict(
                exclude={"relationship"}, exclude_none=True
            )
        )
        if db_idp is None:
            db_idp = create_identity_provider(identity_provider)
        if item.identity_providers.is_connected(db_idp):
            item.identity_providers.replace(
                db_idp, identity_provider.relationship.dict()
            )
        else:
            item.identity_providers.connect(
                db_idp, identity_provider.relationship.dict()
            )


def connect_provider_to_clusters(
    item: models.Provider, clusters: List[schemas.ClusterCreateExtended]
) -> None:
    for cluster in clusters:
        match_name = item.clusters.match(name=cluster.relationship.name).all()
        match_uuid = item.clusters.match(uuid=cluster.relationship.uuid).all()

        if len(match_name) > 1:
            raise
        elif len(match_name) == 1:
            match_name = match_name[0]
        else:
            match_name = None
        if len(match_uuid) > 1:
            raise
        elif len(match_uuid) == 1:
            match_uuid = match_uuid[0]
        else:
            match_uuid = None

        if match_name != match_uuid:
            if match_name is not None:
                item.clusters.disconnect(match_name)
            if match_uuid is not None:
                item.clusters.disconnect(match_uuid)

        replace = False
        new_cluster = schemas.ClusterCreate(**cluster.dict())
        if match_name is not None:
            db_cluster = schemas.ClusterCreate(**match_name.__dict__)
            if db_cluster == new_cluster:
                return db_cluster
            replace = True

        db_clu = read_cluster(**new_cluster.dict())
        if db_clu is None:
            db_clu = create_cluster(new_cluster)
        if item.clusters.is_connected(db_clu) or replace:
            item.clusters.replace(db_clu, cluster.relationship.dict())
        else:
            item.clusters.connect(db_clu, cluster.relationship.dict())


def connect_provider_to_flavors(
    item: models.Provider, flavors: List[schemas.FlavorCreateExtended]
) -> None:
    for flavor in flavors:
        db_flv = read_flavor(
            **flavor.dict(exclude={"relationship"}, exclude_none=True)
        )
        if db_flv is None:
            db_flv = create_flavor(flavor)
        if item.flavors.is_connected(db_flv):
            item.flavors.replace(db_flv, flavor.relationship.dict())
        else:
            item.flavors.connect(db_flv, flavor.relationship.dict())


def connect_provider_to_images(
    item: models.Provider, images: List[schemas.ImageCreateExtended]
) -> None:
    for image in images:
        db_img = read_image(
            **image.dict(exclude={"relationship"}, exclude_none=True)
        )
        if db_img is None:
            db_img = create_image(image)
        if item.images.is_connected(db_img):
            item.images.replace(db_img, image.relationship.dict())
        else:
            item.images.connect(db_img, image.relationship.dict())


def connect_provider_to_location(
    item: models.Provider, location: schemas.LocationCreate
) -> None:
    db_loc = read_location(**location.dict(exclude_none=True))
    if db_loc is None:
        db_loc = create_location(location)
    if not item.location.is_connected(db_loc):
        item.location.connect(db_loc)


def connect_provider_to_projects(
    item: models.Provider, projects: List[schemas.ProjectCreateExtended]
) -> None:
    for project in projects:
        db_proj = read_project(
            **project.dict(exclude={"relationship"}, exclude_none=True)
        )
        if db_proj is None:
            db_proj = create_project(project)
        if item.projects.is_connected(db_proj):
            item.projects.replace(db_proj, project.relationship.dict())
        else:
            item.projects.connect(db_proj, project.relationship.dict())


def connect_provider_to_services(
    item: models.Provider, services: List[schemas.ServiceCreate]
) -> None:
    for service in services:
        db_srv = read_service(endpoint=service.endpoint)
        if db_srv is None:
            db_srv = create_service(service)
        if not item.services.is_connected(db_srv):
            item.services.connect(db_srv)


def create_provider(item: schemas.ProviderCreate) -> models.Provider:
    db_item = models.Provider(
        **item.dict(
            exclude={
                "clusters",
                "flavors",
                "identity_providers",
                "images",
                "location",
                "projects",
                "services",
            }
        )
    ).save()
    if item.location is not None:
        connect_provider_to_location(db_item, item.location)
    if len(item.clusters) > 0:
        connect_provider_to_clusters(db_item, item.clusters)
    if len(item.flavors) > 0:
        connect_provider_to_flavors(db_item, item.flavors)
    if len(item.identity_providers) > 0:
        connect_provider_to_idps(db_item, item.identity_providers)
    if len(item.images) > 0:
        connect_provider_to_images(db_item, item.images)
    if len(item.projects) > 0:
        connect_provider_to_projects(db_item, item.projects)
    if len(item.services) > 0:
        connect_provider_to_services(db_item, item.services)
    return db_item


def read_providers(
    skip: int = 0,
    limit: Optional[int] = None,
    sort: Optional[str] = None,
    **kwargs
) -> List[models.Provider]:
    if kwargs:
        items = models.Provider.nodes.filter(**kwargs).order_by(sort).all()
    else:
        items = models.Provider.nodes.order_by(sort).all()
    return truncate(items=items, skip=skip, limit=limit)


def read_provider(**kwargs) -> Optional[models.Provider]:
    return models.Provider.nodes.get_or_none(**kwargs)


def remove_provider(item: models.Provider) -> bool:
    return item.delete()


def edit_provider(
    old_item: models.Provider, new_item: schemas.ProviderPatch
) -> Optional[models.Provider]:
    for k, v in new_item.dict(
        exclude={
            "clusters",
            "flavors",
            "identity_providers",
            "images",
            "location",
            "projects",
            "services",
        },
        exclude_unset=True,
    ).items():
        old_item.__setattr__(k, v)
    if new_item.location is not None:
        connect_provider_to_location(old_item, new_item.location)
    if len(new_item.clusters) > 0:
        connect_provider_to_clusters(old_item, new_item.clusters)
    if len(new_item.flavors) > 0:
        connect_provider_to_flavors(old_item, new_item.flavors)
    if len(new_item.identity_providers) > 0:
        connect_provider_to_idps(old_item, new_item.identity_providers)
    if len(new_item.images) > 0:
        connect_provider_to_images(old_item, new_item.images)
    if len(new_item.projects) > 0:
        connect_provider_to_projects(old_item, new_item.projects)
    if len(new_item.services) > 0:
        connect_provider_to_services(old_item, new_item.services)
    old_item.save()
    return old_item
