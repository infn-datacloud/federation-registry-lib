from typing import List

from .models import Provider as ProviderModel
from .schemas import ProviderCreate, ProviderUpdate
from .schemas_extended import ProviderCreateExtended
from ..cluster.crud import cluster
from ..cluster.schemas_extended import ClusterCreateExtended
from ..crud import CRUDBase
from ..flavor.crud import flavor
from ..flavor.schemas_extended import FlavorCreateExtended
from ..identity_provider.crud import identity_provider
from ..identity_provider.schemas_extended import IdentityProviderCreateExtended
from ..image.crud import image
from ..image.schemas_extended import ImageCreateExtended
from ..location.crud import location
from ..location.schemas import LocationCreate
from ..project.crud import project
from ..project.schemas_extended import ProjectCreateExtended
from ..service.crud import service
from ..service.schemas_extended import ServiceCreateExtended


class CRUDProvider(CRUDBase[ProviderModel, ProviderCreate, ProviderUpdate]):
    """"""

    def create_and_connect_clusters(
        self, *, db_obj: ProviderModel, new_items: List[ClusterCreateExtended]
    ) -> None:
        for clu in new_items:
            db_cluster = cluster.create(obj_in=clu)
            db_obj.clusters.connect(db_cluster, clu.relationship.dict())

    def create_and_connect_flavors(
        self,
        *,
        db_obj: ProviderModel,
        new_items: List[FlavorCreateExtended],
    ) -> None:
        for flv in new_items:
            db_flavor = flavor.create(obj_in=flv)
            db_obj.flavors.connect(db_flavor, flv.relationship.dict())

    def create_and_connect_identity_providers(
        self,
        *,
        db_obj: ProviderModel,
        new_items: List[IdentityProviderCreateExtended],
    ) -> None:
        for idp in new_items:
            db_identity_provider = identity_provider.create(obj_in=idp)
            db_obj.identity_providers.connect(
                db_identity_provider, idp.relationship.dict()
            )

    def create_and_connect_images(
        self,
        *,
        db_obj: ProviderModel,
        new_items: List[ImageCreateExtended],
    ) -> None:
        for img in new_items:
            db_image = image.create(obj_in=img)
            db_obj.images.connect(db_image, img.relationship.dict())

    def create_and_connect_location(
        self, *, db_obj: ProviderModel, loc: LocationCreate
    ) -> None:
        db_location = location.create(obj_in=loc)
        db_obj.location.connect(db_location)

    def create_and_connect_projects(
        self,
        *,
        db_obj: ProviderModel,
        new_items: List[ProjectCreateExtended],
    ) -> None:
        for proj in new_items:
            db_project = project.create(obj_in=proj, force=True)
            db_obj.projects.connect(db_project, proj.relationship.dict())

    def create_and_connect_services(
        self, *, db_obj: ProviderModel, new_items: List[ServiceCreateExtended]
    ) -> None:
        for srv in new_items:
            db_srv = service.create_with_type(obj_in=srv)
            db_obj.services.connect(db_srv)

    def create_with_all(
        self, *, obj_in: ProviderCreateExtended
    ) -> ProviderModel:
        db_obj = self.create(obj_in=obj_in)
        if obj_in.location is not None:
            self.create_and_connect_location(
                db_obj=db_obj, loc=obj_in.location
            )
        self.create_and_connect_clusters(
            db_obj=db_obj, new_items=obj_in.clusters
        )
        self.create_and_connect_flavors(
            db_obj=db_obj, new_items=obj_in.flavors
        )
        self.create_and_connect_identity_providers(
            db_obj=db_obj, new_items=obj_in.identity_providers
        )
        self.create_and_connect_images(db_obj=db_obj, new_items=obj_in.images)
        self.create_and_connect_projects(
            db_obj=db_obj, new_items=obj_in.projects
        )
        self.create_and_connect_services(
            db_obj=db_obj, new_items=obj_in.services
        )
        return db_obj


provider = CRUDProvider(ProviderModel, ProviderCreate)


#
# from . import models, schemas_extended
#
# from typing import Any, Callable, List, Optional
# from neomodel import StructuredNode, RelationshipManager
# from pydantic import BaseModel
#
#
# def check_rel_name_uuid_consist_connection(
#    rel_manager: RelationshipManager, new_end_node: BaseModel
# ):
#    end_node_rel_match_name = rel_manager.match(
#        name=new_end_node.relationship.name
#    ).all()
#    end_node_rel_match_uuid = rel_manager.match(
#        uuid=new_end_node.relationship.uuid
#    ).all()
#
#    if len(end_node_rel_match_name) > 1:
#        raise  # TODO
#    elif len(end_node_rel_match_name) == 1:
#        end_node_rel_match_name = end_node_rel_match_name[0]
#    else:
#        end_node_rel_match_name = None
#    if len(end_node_rel_match_uuid) > 1:
#        raise  # TODO
#    elif len(end_node_rel_match_uuid) == 1:
#        end_node_rel_match_uuid = end_node_rel_match_uuid[0]
#    else:
#        end_node_rel_match_uuid = None
#
#    if end_node_rel_match_name != end_node_rel_match_uuid or (
#        end_node_rel_match_name is not None
#        and (
#            rel_manager.relationship(end_node_rel_match_name).uuid
#            != rel_manager.relationship(end_node_rel_match_uuid).uuid
#            or rel_manager.relationship(end_node_rel_match_uuid).name
#            != rel_manager.relationship(end_node_rel_match_name).name
#        )
#    ):
#        if end_node_rel_match_name is not None:
#            rel_manager.disconnect(end_node_rel_match_name)
#        if end_node_rel_match_uuid is not None:
#            rel_manager.disconnect(end_node_rel_match_uuid)
#        return None
#
#    return end_node_rel_match_name
#
#
# def create_and_connect(
#    rel_manager: RelationshipManager,
#    new_end_node: BaseModel,
#    read_func: Callable,
#    create_func: Callable,
# ):
#    db_clu = read_func(
#        **new_end_node.dict(exclude={"relationship"}, exclude_none=True)
#    )
#    if db_clu is None:
#        db_clu = create_func(new_end_node)
#        rel_manager.connect(db_clu, new_end_node.relationship.dict())
#    else:
#        rel_manager.replace(db_clu, new_end_node.relationship.dict())
#
#
# def create_and_replace(
#    rel_manager: RelationshipManager,
#    new_end_node: BaseModel,
#    read_func: Callable,
#    create_func: Callable,
# ):
#    db_clu = read_func(
#        **new_end_node.dict(exclude={"relationship"}, exclude_none=True)
#    )
#    if db_clu is None:
#        db_clu = create_func(new_end_node)
#        rel_manager.replace(db_clu, new_end_node.relationship.dict())
#    else:
#        rel_manager.connect(db_clu, new_end_node.relationship.dict())
#
#
# def connect_provider_to_clusters(
#    item: models.Provider,
#    clusters: List[schemas_extended.ClusterCreateExtended],
# ) -> None:
#    for cluster in clusters:
#        db_cluster = check_rel_name_uuid_consist_connection(
#            item.clusters, cluster
#        )
#        if db_cluster is not None:
#            new_cluster = schemas_extended.ClusterCreate(
#                **cluster.dict(exclude={"relationship"})
#            )
#            old_cluster = schemas_extended.ClusterCreate(**db_cluster.__dict__)
#            if old_cluster != new_cluster:
#                create_and_replace(
#                    rel_manager=item.clusters,
#                    new_end_node=cluster,
#                    read_func=cluster.get,
#                    create_func=cluster.create,
#                )
#        else:
#            create_and_connect(
#                rel_manager=item.clusters,
#                new_end_node=cluster,
#                read_func=cluster.get,
#                create_func=cluster.create,
#            )
#
#
# def connect_provider_to_flavors(
#    item: models.Provider, flavors: List[schemas_extended.FlavorCreateExtended]
# ) -> None:
#    for flavor in flavors:
#        db_flavor = check_rel_name_uuid_consist_connection(
#            item.flavors, flavor
#        )
#        if db_flavor is not None:
#            new_flavor = schemas_extended.ClusterCreate(
#                **flavor.dict(exclude={"relationship"})
#            )
#            old_flavor = schemas_extended.ClusterCreate(**db_flavor.__dict__)
#            if old_flavor != new_flavor:
#                create_and_replace(
#                    rel_manager=item.flavors,
#                    new_end_node=flavor,
#                    read_func=flavor.get,
#                    create_func=flavor.create,
#                )
#        else:
#            create_and_connect(
#                rel_manager=item.flavors,
#                new_end_node=flavor,
#                read_func=flavor.get,
#                create_func=flavor.create,
#            )
#
#
# def connect_provider_to_idps(
#    item: models.Provider,
#    identity_providers: List[schemas_extended.IdentityProviderCreateExtended],
# ) -> None:
#    for identity_provider in identity_providers:
#        db_idp = identity_provider.get(
#            **identity_provider.dict(
#                exclude={"relationship"}, exclude_none=True
#            )
#        )
#        if db_idp is None:
#            db_idp = identity_provider.create(identity_provider)
#        if item.identity_providers.is_connected(db_idp):
#            item.identity_providers.replace(
#                db_idp, identity_provider.relationship.dict()
#            )
#        else:
#            item.identity_providers.connect(
#                db_idp, identity_provider.relationship.dict()
#            )
#
#
# def connect_provider_to_images(
#    item: models.Provider, images: List[schemas_extended.ImageCreateExtended]
# ) -> None:
#    for image in images:
#        db_image = check_rel_name_uuid_consist_connection(item.images, image)
#        if db_image is not None:
#            new_image = schemas_extended.ClusterCreate(
#                **image.dict(exclude={"relationship"})
#            )
#            old_image = schemas_extended.ClusterCreate(**db_image.__dict__)
#            if old_image != new_image:
#                create_and_replace(
#                    rel_manager=item.images,
#                    new_end_node=image,
#                    read_func=image.get,
#                    create_func=image.create,
#                )
#        else:
#            create_and_connect(
#                rel_manager=item.images,
#                new_end_node=image,
#                read_func=image.get,
#                create_func=image.create,
#            )
#
#
# def connect_provider_to_location(
#    item: models.Provider, location: schemas_extended.LocationCreate
# ) -> None:
#    db_loc = location.get(**location.dict(exclude_none=True))
#    if db_loc is None:
#        db_loc = location.create(location)
#    if not item.location.is_connected(db_loc):
#        item.location.connect(db_loc)
#
#
# def connect_provider_to_projects(
#    item: models.Provider,
#    projects: List[schemas_extended.ProjectCreateExtended],
# ) -> None:
#    for project in projects:
#        db_project = check_rel_name_uuid_consist_connection(
#            item.projects, project
#        )
#        if db_project is not None:
#            new_project = schemas_extended.ClusterCreate(
#                **project.dict(exclude={"relationship"})
#            )
#            old_project = schemas_extended.ClusterCreate(**db_project.__dict__)
#            if old_project != new_project:
#                create_and_replace(
#                    rel_manager=item.projects,
#                    new_end_node=project,
#                    read_func=project.get,
#                    create_func=project.create,
#                )
#        else:
#            create_and_connect(
#                rel_manager=item.projects,
#                new_end_node=project,
#                read_func=project.get,
#                create_func=project.create,
#            )
#
#
# def connect_provider_to_services(
#    item: models.Provider, services: List[schemas_extended.ServiceCreate]
# ) -> None:
#    for service in services:
#        db_srv = service.get(endpoint=service.endpoint)
#        if db_srv is None:
#            db_srv = service.create(service)
#        if not item.services.is_connected(db_srv):
#            item.services.connect(db_srv)
#
#
# def read_providers(
#    skip: int = 0,
#    limit: Optional[int] = None,
#    sort: Optional[str] = None,
#    **kwargs,
# ) -> List[models.Provider]:
#    if kwargs:
#        items = models.Provider.nodes.filter(**kwargs).order_by(sort).all()
#    else:
#        items = models.Provider.nodes.order_by(sort).all()
#    return truncate(items=items, skip=skip, limit=limit)
#
#
# def read_provider(**kwargs) -> Optional[models.Provider]:
#    return models.Provider.nodes.get_or_none(**kwargs)
#
#
# def remove_provider(item: models.Provider) -> bool:
#    return item.delete()
#
#
# def edit_provider(
#    old_item: models.Provider, new_item: schemas_extended.ProviderUpdate
# ) -> Optional[models.Provider]:
#    for k, v in new_item.dict(
#        exclude={
#            "clusters",
#            "flavors",
#            "identity_providers",
#            "images",
#            "location",
#            "projects",
#            "services",
#        },
#        exclude_unset=True,
#    ).items():
#        old_item.__setattr__(k, v)
#    if new_item.location is not None:
#        connect_provider_to_location(old_item, new_item.location)
#    if len(new_item.clusters) > 0:
#        connect_provider_to_clusters(old_item, new_item.clusters)
#    if len(new_item.flavors) > 0:
#        connect_provider_to_flavors(old_item, new_item.flavors)
#    if len(new_item.identity_providers) > 0:
#        connect_provider_to_idps(old_item, new_item.identity_providers)
#    if len(new_item.images) > 0:
#        connect_provider_to_images(old_item, new_item.images)
#    if len(new_item.projects) > 0:
#        connect_provider_to_projects(old_item, new_item.projects)
#    if len(new_item.services) > 0:
#        connect_provider_to_services(old_item, new_item.services)
#    old_item.save()
#    return old_item
#
