from typing import List, Optional

from .cluster import create_cluster, read_cluster
from .flavor import create_flavor, read_flavor
from .identity_provider import create_identity_provider, read_identity_provider
from .image import create_image, read_image
from .location import create_location, read_location
from .project import create_project, read_project
from .service import create_service, read_service
from .utils import (
    check_rel_name_uuid_consist_connection,
    create_and_connect,
    create_and_replace,
    truncate,
)
from .. import schemas, models


def connect_provider_to_clusters(
    item: models.Provider, clusters: List[schemas.ClusterCreateExtended]
) -> None:
    for cluster in clusters:
        db_cluster = check_rel_name_uuid_consist_connection(
            item.clusters, cluster
        )
        if db_cluster is not None:
            new_cluster = schemas.ClusterCreate(
                **cluster.dict(exclude={"relationship"})
            )
            old_cluster = schemas.ClusterCreate(**db_cluster.__dict__)
            if old_cluster != new_cluster:
                create_and_replace(
                    rel_manager=item.clusters,
                    new_end_node=cluster,
                    read_func=read_cluster,
                    create_func=create_cluster,
                )
        else:
            create_and_connect(
                rel_manager=item.clusters,
                new_end_node=cluster,
                read_func=read_cluster,
                create_func=create_cluster,
            )


def connect_provider_to_flavors(
    item: models.Provider, flavors: List[schemas.FlavorCreateExtended]
) -> None:
    for flavor in flavors:
        db_flavor = check_rel_name_uuid_consist_connection(
            item.flavors, flavor
        )
        if db_flavor is not None:
            new_flavor = schemas.ClusterCreate(
                **flavor.dict(exclude={"relationship"})
            )
            old_flavor = schemas.ClusterCreate(**db_flavor.__dict__)
            if old_flavor != new_flavor:
                create_and_replace(
                    rel_manager=item.flavors,
                    new_end_node=flavor,
                    read_func=read_flavor,
                    create_func=create_flavor,
                )
        else:
            create_and_connect(
                rel_manager=item.flavors,
                new_end_node=flavor,
                read_func=read_flavor,
                create_func=create_flavor,
            )


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


def connect_provider_to_images(
    item: models.Provider, images: List[schemas.ImageCreateExtended]
) -> None:
    for image in images:
        db_image = check_rel_name_uuid_consist_connection(item.images, image)
        if db_image is not None:
            new_image = schemas.ClusterCreate(
                **image.dict(exclude={"relationship"})
            )
            old_image = schemas.ClusterCreate(**db_image.__dict__)
            if old_image != new_image:
                create_and_replace(
                    rel_manager=item.images,
                    new_end_node=image,
                    read_func=read_image,
                    create_func=create_image,
                )
        else:
            create_and_connect(
                rel_manager=item.images,
                new_end_node=image,
                read_func=read_image,
                create_func=create_image,
            )


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
        db_project = check_rel_name_uuid_consist_connection(
            item.projects, project
        )
        if db_project is not None:
            new_project = schemas.ClusterCreate(
                **project.dict(exclude={"relationship"})
            )
            old_project = schemas.ClusterCreate(**db_project.__dict__)
            if old_project != new_project:
                create_and_replace(
                    rel_manager=item.projects,
                    new_end_node=project,
                    read_func=read_project,
                    create_func=create_project,
                )
        else:
            create_and_connect(
                rel_manager=item.projects,
                new_end_node=project,
                read_func=read_project,
                create_func=create_project,
            )


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
        get_or_create_and_connect_location(db_item, item.location)
    get_or_create_and_connect_clusters(db_item, item.clusters)
    get_or_create_and_connect_flavors(db_item, item.flavors)
    get_or_create_and_connect_identity_providers(
        db_item, item.identity_providers
    )
    get_or_create_and_connect_images(db_item, item.images)
    get_or_create_and_connect_projects(db_item, item.projects)
    get_or_create_and_connect_services(db_item, item.services)
    return db_item


def get_or_create_and_connect_clusters(
    item: models.Provider, new_clusters: List[schemas.ClusterCreateExtended]
) -> None:
    for cluster in new_clusters:
        db_cluster = create_cluster(cluster)
        item.clusters.connect(db_cluster, cluster.relationship.dict())


def get_or_create_and_connect_flavors(
    item: models.Provider, new_flavors: List[schemas.FlavorCreateExtended]
) -> None:
    for flavor in new_flavors:
        db_flavor = create_flavor(flavor)
        item.flavors.connect(db_flavor, flavor.relationship.dict())


def get_or_create_and_connect_identity_providers(
    item: models.Provider,
    new_identity_providers: List[schemas.IdentityProviderCreateExtended],
) -> None:
    for identity_provider in new_identity_providers:
        db_identity_provider = create_identity_provider(identity_provider)
        item.identity_providers.connect(
            db_identity_provider, identity_provider.relationship.dict()
        )


def get_or_create_and_connect_images(
    item: models.Provider, new_images: List[schemas.ImageCreateExtended]
) -> None:
    for image in new_images:
        db_image = create_image(image)
        item.images.connect(db_image, image.relationship.dict())


def get_or_create_and_connect_location(
    item: models.Provider, location: schemas.LocationCreate
) -> None:
    db_location = create_location(location)
    item.location.connect(db_location)


def get_or_create_and_connect_projects(
    item: models.Provider, new_projects: List[schemas.ProjectCreateExtended]
) -> None:
    for project in new_projects:
        db_project = create_project(project)
        item.projects.connect(db_project, project.relationship.dict())


def get_or_create_and_connect_services(
    item: models.Provider, new_services: List[schemas.ServiceCreate]
) -> None:
    for service in new_services:
        db_srv = read_service(endpoint=service.endpoint)
        if db_srv is None:
            db_srv = create_service(service)
        if not item.services.is_connected(db_srv):
            item.services.connect(db_srv)


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
