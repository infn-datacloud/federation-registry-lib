import os

import requests
from crud import (
    FlavorPopulation,
    IdentityProviderPopulation,
    ImagePopulation,
    LocationPopulation,
    ProjectPopulation,
    ProviderPopulation,
    QuotaPopulation,
    ServicePopulation,
)
from fastapi import status
from logger import logger
from models.cmdb import ProviderRead, ProviderWrite, URLs
from pydantic import AnyHttpUrl

crud_image = ImagePopulation()
crud_flavor = FlavorPopulation()
crud_project = ProjectPopulation()
crud_provider = ProviderPopulation()
crud_location = LocationPopulation()
crud_identity_provider = IdentityProviderPopulation()
crud_service = ServicePopulation()
crud_quota = QuotaPopulation()


def add_or_patch_provider(
    *,
    provider: ProviderWrite,
    token: str,
    url: AnyHttpUrl,
    api_ver_flavors: str = "v1",
    api_ver_identity_providers: str = "v1",
    api_ver_images: str = "v1",
    api_ver_locations: str = "v1",
    api_ver_projects: str = "v1",
    api_ver_providers: str = "v1",
    api_ver_quotas: str = "v1",
    api_ver_services: str = "v1",
    api_ver_slas: str = "v1",
    api_ver_user_groups: str = "v1",
) -> None:
    """Add a new provider to the CMDB with the given attributes."""

    read_header = {"Authorization": f"Bearer {token}"}
    write_header = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    urls = URLs(
        flavors=os.path.join(url, f"api/{api_ver_flavors}/flavors/"),
        identity_providers=os.path.join(
            url, f"api/{api_ver_identity_providers}/identity_providers/"
        ),
        images=os.path.join(url, f"api/{api_ver_images}/images/"),
        locations=os.path.join(url, f"api/{api_ver_locations}/locations/"),
        projects=os.path.join(url, f"api/{api_ver_projects}/projects/"),
        providers=os.path.join(url, f"api/{api_ver_providers}/providers/"),
        quotas=os.path.join(url, f"api/{api_ver_quotas}/quotas"),
        services=os.path.join(url, f"api/{api_ver_services}/services/"),
        slas=os.path.join(url, f"api/{api_ver_slas}/slas/"),
        user_groups=os.path.join(url, f"api/{api_ver_user_groups}/user_groups/"),
    )

    logger.info(f"Adding provider {provider.name} to CMDB")
    resp = requests.get(
        url=urls.providers,
        params={"name": provider.name, "with_conn": True},
        headers=read_header,
    )
    if resp.status_code == status.HTTP_200_OK:
        provider_list = resp.json()

        if len(provider_list) == 0:
            logger.info(f"No match found. Creating new provider '{provider.name}'")
            db_provider = crud_provider.create(
                new_data=provider, url=urls.providers, header=write_header
            )

        elif len(provider_list) == 1:
            logger.info(f"One match found. Trying to update provider '{provider.name}'")
            db_provider = ProviderRead(**provider_list[0])
            url = os.path.join(urls.providers, str(db_provider.uid))
            crud_provider.update(new_data=provider, url=url, header=write_header)

            for flavor in provider.flavors:
                db_flavor = crud_flavor.find_in_list(
                    key="name", value=flavor.name, db_items=db_provider.flavors
                )
                if db_flavor is None:
                    db_flavor = crud_flavor.find_in_list(
                        key="uuid", value=flavor.uuid, db_items=db_provider.flavors
                    )
                if db_flavor is not None:
                    logger.info(f"Trying to update flavor '{flavor.name}'.")
                    url = os.path.join(urls.flavors, str(db_flavor.uid))
                    crud_flavor.update(new_data=flavor, url=url, header=write_header)
                else:
                    logger.info(f"Creating new flavor '{flavor.name}'.")
                    url = os.path.join(urls.providers, str(db_provider.uid), "flavors")
                    db_flavor = crud_flavor.create(
                        new_data=flavor, url=url, header=write_header
                    )

            for image in provider.images:
                db_image = crud_image.find_in_list(
                    key="name", value=image.name, db_items=db_provider.images
                )
                if db_image is None:
                    db_image = crud_image.find_in_list(
                        key="uuid", value=image.uuid, db_items=db_provider.images
                    )
                if db_image is not None:
                    logger.info(f"Trying to update image '{image.name}'.")
                    url = os.path.join(urls.images, str(db_image.uid))
                    crud_image.update(new_data=image, url=url, header=write_header)
                else:
                    logger.info(f"Creating new image '{image.name}'.")
                    url = os.path.join(urls.providers, str(db_provider.uid), "images")
                    db_image = crud_image.create(
                        new_data=image, url=url, header=write_header
                    )

            for service in provider.services:
                db_service = crud_service.find_in_list(
                    key="name", value=service.name, db_items=db_provider.services
                )
                if db_service is not None:
                    logger.info(f"Trying to update service '{service.name}'.")
                    url = os.path.join(urls.services, str(db_service.uid))
                    crud_service.update(new_data=service, url=url, header=write_header)
                else:
                    logger.info(f"Creating new service '{service.name}'.")
                    url = os.path.join(urls.providers, str(db_provider.uid), "services")
                    db_service = crud_service.create(
                        new_data=service, url=url, header=write_header
                    )

                if db_service.type == "compute":
                    compute_service_uid = db_service.uid
                # elif db_service.type == "block-storage":
                #    block_storage_service_uid = db_service.uid

            for project in provider.projects:
                db_project = crud_project.find_in_list(
                    key="name", value=project.name, db_items=db_provider.projects
                )
                if db_project is None:
                    db_project = crud_project.find_in_list(
                        key="uuid", value=project.uuid, db_items=db_provider.projects
                    )
                if db_project is not None:
                    logger.info(f"Trying to update project '{project.name}'.")
                    url = os.path.join(urls.projects, str(db_project.uid))
                    crud_project.update(new_data=project, url=url, header=write_header)
                else:
                    logger.info(f"Creating new project '{project.name}'.")
                    url = os.path.join(urls.providers, str(db_provider.uid), "projects")
                    db_project = crud_project.create(
                        new_data=project, url=url, header=write_header
                    )

                # Connect quotas
                db_project = crud_project.find(
                    url=urls.projects, header=read_header, params={"name": project.name}
                )  # TODO Modify provider schema such that project contains quotas?
                if len(db_project.quotas) == 0:
                    logger.info("Creating new set of quotas.")
                    crud_quota.create(
                        new_data=project.compute_quota,
                        url=urls.quotas,
                        header=write_header,
                        params={
                            "project_uid": db_project.uid,
                            "service_uid": compute_service_uid,
                        },
                    )
                else:
                    # TODO Update existing
                    pass

            for identity_provider in provider.identity_providers:
                db_identity_provider = crud_identity_provider.find(
                    url=urls.identity_providers,
                    header=read_header,
                    params={"endpoint": identity_provider.endpoint},
                )
                if db_identity_provider is None:
                    logger.info(
                        "Creating new identity provider "
                        f"'{identity_provider.endpoint}'."
                    )
                    db_identity_provider = crud_identity_provider.create(
                        new_data=identity_provider,
                        url=urls.identity_providers,
                        header=write_header,
                    )
                else:
                    logger.info(
                        "Trying to update identity provider "
                        f"'{identity_provider.endpoint}'."
                    )
                    url = os.path.join(
                        urls.identity_providers, str(db_identity_provider.uid)
                    )
                    crud_identity_provider.update(
                        new_data=identity_provider, url=url, header=write_header
                    )
                logger.info(
                    f"Connecting identity provider '{identity_provider.endpoint}'."
                )
                url = os.path.join(
                    urls.providers,
                    str(db_provider.uid),
                    "identity_providers",
                    str(db_identity_provider.uid),
                )
                crud_identity_provider.connect(
                    url=url, header=write_header, new_data=identity_provider
                )

            if provider.location is not None:
                db_location = crud_location.find(
                    url=urls.locations,
                    header=read_header,
                    params={"name": provider.location.name},
                )
                if db_location is None:
                    logger.info(f"Creating new location '{provider.location.name}'.")
                    db_location = crud_location.create(
                        new_data=provider.location,
                        url=urls.locations,
                        header=write_header,
                    )
                else:
                    logger.info(
                        f"Trying to update location '{provider.location.name}'."
                    )
                    url = os.path.join(urls.locations, str(db_location.uid))
                    crud_location.update(
                        new_data=provider.location, url=url, header=write_header
                    )
                logger.info(f"Connecting location '{provider.location.name}'.")
                url = os.path.join(
                    urls.providers,
                    str(db_provider.uid),
                    "locations",
                    str(db_location.uid),
                )
                crud_location.connect(
                    url=url, header=write_header, new_data=provider.location
                )

        # Multiple matches -> DB Corrupted
        else:
            logger.error(f"Multiple providers with the same name '{provider.name}'")
