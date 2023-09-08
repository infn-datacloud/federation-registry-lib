import os

import requests
from crud import (
    FlavorPopulation,
    ImagePopulation,
    ProjectPopulation,
    ProviderPopulation,
)
from fastapi import status
from logger import logger
from models.cmdb import ProviderRead, ProviderWrite, URLs
from pydantic import AnyHttpUrl

crud_image = ImagePopulation()
crud_flavor = FlavorPopulation()
crud_project = ProjectPopulation()
crud_provider = ProviderPopulation()


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
            crud_provider.create(
                new_data=provider, url=urls.providers, header=write_header
            )

        elif len(provider_list) == 1:
            logger.info(f"One match found. Trying to update provider '{provider.name}'")
            db_provider = ProviderRead(**provider_list[0])
            url = os.path.join(urls.providers, str(db_provider.uid))
            crud_provider.update(new_data=provider, url=url, header=write_header)

            for flavor in provider.flavors:
                db_flavor = crud_flavor.find(
                    new_data=flavor, db_items=db_provider.flavors
                )
                if db_flavor is not None:
                    logger.info(f"Trying to update flavor '{flavor.name}'.")
                    url = os.path.join(urls.flavors, str(db_flavor.uid))
                    crud_flavor.update(new_data=flavor, url=url, header=write_header)
                else:
                    logger.info(f"Creating new flavor '{flavor.name}'.")
                    url = os.path.join(urls.providers, str(db_provider.uid), "flavors")
                    crud_flavor.create(new_data=flavor, url=url, header=write_header)

            for image in provider.images:
                db_image = crud_image.find(new_data=image, db_items=db_provider.images)
                if db_image is not None:
                    logger.info(f"Trying to update image '{image.name}'.")
                    url = os.path.join(urls.images, str(db_image.uid))
                    crud_image.update(new_data=image, url=url, header=write_header)
                else:
                    logger.info(f"Creating new image '{image.name}'.")
                    url = os.path.join(urls.providers, str(db_provider.uid), "images")
                    crud_image.create(new_data=image, url=url, header=write_header)

            for project in provider.projects:
                db_project = crud_project.find(
                    new_data=project, db_items=db_provider.projects
                )
                if db_project is not None:
                    logger.info(f"Trying to update project '{project.name}'.")
                    url = os.path.join(urls.projects, str(db_project.uid))
                    crud_project.update(new_data=project, url=url, header=write_header)
                else:
                    logger.info(f"Creating new project '{project.name}'.")
                    url = os.path.join(urls.providers, str(db_provider.uid), "projects")
                    crud_project.create(new_data=project, url=url, header=write_header)

        # Multiple matches -> DB Corrupted
        else:
            logger.error(f"Multiple providers with the same name '{provider.name}'")
