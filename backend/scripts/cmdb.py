from crud import CRUDs
from logger import logger
from models.cmdb import ProjectQuery, ProviderQuery, ProviderWrite


def add_or_patch_provider(*, provider: ProviderWrite, cruds: CRUDs) -> None:
    """Add a new provider to the CMDB with the given attributes."""
    logger.info(f"Adding or updating {provider} to CMDB")
    db_provider = cruds.providers.single(
        data=ProviderQuery(name=provider.name), with_conn=True
    )
    if db_provider is None:
        db_provider = cruds.providers.create(new_data=provider)
    else:
        db_provider = cruds.providers.update(new_data=provider, old_data=db_provider)

        for flavor in provider.flavors:
            cruds.flavors.create_or_update(item=flavor, parent=db_provider)

        for image in provider.images:
            cruds.images.create_or_update(item=image, parent=db_provider)

        for service in provider.services:
            db_service = cruds.services.create_or_update(
                item=service, parent=db_provider
            )
            for project in provider.projects:
                if db_service.type == "compute":
                    project.compute_quota.service = db_service.uid
                if db_service.type == "block-storage":
                    project.block_storage_quota.service = db_service.uid

        for project in provider.projects:
            db_project = cruds.projects.create_or_update(
                item=project, parent=db_provider
            )

            db_project = cruds.projects.single(
                data=ProjectQuery(name=project.name), with_conn=True
            )
            for quota in [project.compute_quota, project.block_storage_quota]:
                cruds.quotas.create_or_update(item=quota, parent=db_project)

        for identity_provider in provider.identity_providers:
            cruds.identity_providers.create_or_update(
                item=identity_provider, parent=db_provider
            )

        if provider.location is not None:
            cruds.locations.create_or_update(item=provider.location, parent=db_provider)
