from typing import List, Optional

from .cluster import create_cluster, get_cluster
from .flavor import create_flavor, get_flavor
from .identity_provider import create_identity_provider, get_identity_provider
from .image import create_image, get_image
from .location import create_location, get_location
from .service import create_service, get_service
from .. import schemas, models


def connect_provider_to_idps(
    item: models.Provider,
    identity_providers: List[schemas.ProviderClusterCreate],
) -> None:
    for identity_provider in identity_providers:
        db_img = get_identity_provider(
            **identity_provider.dict(
                exclude={"relationship"}, exclude_none=True
            )
        )
        if db_img is None:
            db_img = create_identity_provider(identity_provider)
        if item.identity_providers.is_connected(db_img):
            item.identity_providers.replace(
                db_img, identity_provider.relationship.dict()
            )
        else:
            item.identity_providers.connect(
                db_img, identity_provider.relationship.dict()
            )


def connect_provider_to_clusters(
    item: models.Provider,
    clusters: List[schemas.ProviderClusterCreate],
) -> None:
    for cluster in clusters:
        db_img = get_cluster(
            **cluster.dict(exclude={"relationship"}, exclude_none=True)
        )
        if db_img is None:
            db_img = create_cluster(cluster)
        if item.clusters.is_connected(db_img):
            item.clusters.replace(db_img, cluster.relationship.dict())
        else:
            item.clusters.connect(db_img, cluster.relationship.dict())


def connect_provider_to_flavors(
    item: models.Provider,
    flavors: List[schemas.ProviderFlavorCreate],
) -> None:
    for flavor in flavors:
        db_img = get_flavor(
            **flavor.dict(exclude={"relationship"}, exclude_none=True)
        )
        if db_img is None:
            db_img = create_flavor(flavor)
        if item.flavors.is_connected(db_img):
            item.flavors.replace(db_img, flavor.relationship.dict())
        else:
            item.flavors.connect(db_img, flavor.relationship.dict())


def connect_provider_to_images(
    item: models.Provider,
    images: List[schemas.ProviderImageCreate],
) -> None:
    for image in images:
        db_img = get_image(
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
    db_loc = get_location(**location.dict(exclude_none=True))
    if db_loc is None:
        db_loc = create_location(location)
    if not item.location.is_connected(db_loc):
        item.location.connect(db_loc)


def connect_provider_to_services(
    item: models.Provider,
    services: List[schemas.ProviderServiceCreate],
) -> None:
    for service in services:
        db_img = get_service(
            **service.dict(exclude={"relationship"}, exclude_none=True)
        )
        if db_img is None:
            db_img = create_service(service)
        if item.services.is_connected(db_img):
            item.services.replace(db_img, service.relationship.dict())
        else:
            item.services.connect(db_img, service.relationship.dict())


def create_provider(item: schemas.ProviderCreate) -> models.Provider:
    db_item = models.Provider(
        **item.dict(
            exclude={
                "clusters",
                "flavors",
                "identity_providers",
                "images",
                "location",
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
    if len(item.services) > 0:
        connect_provider_to_services(db_item, item.services)
    return db_item


def get_providers(
    skip: int = 0,
    limit: Optional[int] = None,
    sort: Optional[str] = None,
    **kwargs
) -> List[models.Provider]:
    if kwargs:
        items = models.Provider.nodes.filter(**kwargs).order_by(sort).all()
    else:
        items = models.Provider.nodes.order_by(sort).all()
    if limit is None:
        return items[skip:]
    return items[skip : skip + limit]


def get_provider(**kwargs) -> Optional[models.Provider]:
    return models.Provider.nodes.get_or_none(**kwargs)


def remove_provider(item: models.Provider) -> bool:
    return item.delete()


def update_provider(
    old_item: models.Provider, new_item: schemas.ProviderUpdate
) -> Optional[models.Provider]:
    for k, v in new_item.dict(
        exclude={
            "clusters",
            "flavors",
            "identity_providers",
            "images",
            "location",
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
    if len(old_item.services) > 0:
        connect_provider_to_services(old_item, new_item.services)
    old_item.save()
    return old_item
