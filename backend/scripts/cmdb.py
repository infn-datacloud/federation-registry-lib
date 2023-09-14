from crud import CRUDs
from logger import logger
from models.cmdb import ProviderWrite


def add_or_patch_provider(*, provider: ProviderWrite, cruds: CRUDs) -> None:
    """Add a new provider to the CMDB with the given attributes."""
    logger.info(f"Adding or updating provider {provider.name} to CMDB")
    db_provider = cruds.providers.single(
        params={"name": provider.name, "with_conn": True}
    )
    if db_provider is None:
        db_provider = cruds.providers.create(new_data=provider)
    else:
        db_provider = cruds.providers.update(
            new_data=provider, old_data=db_provider, uid=db_provider.uid
        )

        for flavor in provider.flavors:
            db_flavor = cruds.flavors.find_in_list(
                key="name", value=flavor.name, db_items=db_provider.flavors
            )
            if db_flavor is None:
                db_flavor = cruds.flavors.find_in_list(
                    key="uuid", value=flavor.uuid, db_items=db_provider.flavors
                )
            if db_flavor is None:
                db_flavor = cruds.flavors.create(
                    new_data=flavor, parent_uid=db_provider.uid
                )
            else:
                db_flavor = cruds.flavors.update(
                    new_data=flavor, uid=db_flavor.uid, old_data=db_flavor
                )

        for image in provider.images:
            db_image = cruds.images.find_in_list(
                key="name", value=image.name, db_items=db_provider.images
            )
            if db_image is None:
                db_image = cruds.images.find_in_list(
                    key="uuid", value=image.uuid, db_items=db_provider.images
                )
            if db_image is None:
                db_image = cruds.images.create(
                    new_data=image, parent_uid=db_provider.uid
                )
            else:
                db_image = cruds.images.update(
                    new_data=image, uid=db_image.uid, old_data=db_image
                )

        for service in provider.services:
            db_service = cruds.services.find_in_list(
                key="name", value=service.name, db_items=db_provider.services
            )
            if db_service is None:
                db_service = cruds.services.create(
                    new_data=service, parent_uid=db_provider.uid
                )
            else:
                db_service = cruds.services.update(
                    new_data=service, uid=db_service.uid, old_data=db_service
                )

        for project in provider.projects:
            db_project = cruds.projects.find_in_list(
                key="name", value=project.name, db_items=db_provider.projects
            )
            if db_project is None:
                db_project = cruds.projects.find_in_list(
                    key="uuid", value=project.uuid, db_items=db_provider.projects
                )
            if db_project is None:
                db_project = cruds.projects.create(
                    new_data=project, parent_uid=db_provider.uid
                )
            else:
                db_project = cruds.projects.update(
                    new_data=project, uid=db_project.uid, old_data=db_project
                )

            # Connect quotas
            # TODO Modify provider schema such that project contains quotas
            # or Quotas contains Service?
            db_project = cruds.projects.single(
                params={"name": project.name, "with_conn": True}
            )
            for quota in [project.compute_quota, project.block_storage_quota]:
                db_quota = cruds.quotas.find_in_list(
                    key="type", value=quota.type, db_items=db_project.quotas
                )
                if db_quota is None:
                    idx = [s.name for s in db_provider.services].index(quota.type)
                    service_uid = db_provider.services[idx].uid
                    db_quota = cruds.quotas.create(
                        new_data=quota,
                        params={
                            "project_uid": db_project.uid,
                            "service_uid": service_uid,
                        },
                    )
                else:
                    db_quota = cruds.quotas.update(
                        new_data=quota, uid=db_quota.uid, old_data=db_quota
                    )

        for identity_provider in provider.identity_providers:
            db_identity_provider = cruds.identity_providers.single(
                params={"endpoint": identity_provider.endpoint},
            )
            if db_identity_provider is None:
                db_identity_provider = cruds.identity_providers.create(
                    new_data=identity_provider
                )
            else:
                db_identity_provider = cruds.identity_providers.update(
                    new_data=identity_provider,
                    uid=db_identity_provider.uid,
                    old_data=db_identity_provider,
                )
            cruds.identity_providers.connect(
                uid=db_identity_provider.uid,
                parent_uid=db_provider.uid,
                new_data=identity_provider,
            )

        if provider.location is not None:
            db_location = cruds.locations.single(
                params={"name": provider.location.name},
            )
            if db_location is None:
                db_location = cruds.locations.create(new_data=provider.location)
            else:
                db_location = cruds.locations.update(
                    new_data=provider.location,
                    uid=db_location.uid,
                    old_data=db_location,
                )
            cruds.locations.connect(
                uid=db_location.uid,
                parent_uid=db_provider.uid,
                new_data=provider.location,
            )
