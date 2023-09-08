import os

import requests
from fastapi import status
from fastapi.encoders import jsonable_encoder
from models.cmdb import Provider, ProviderRead


def add_or_patch_provider(
    *,
    url: str,
    provider: Provider,
    token: str,
    api_ver_providers: str = "v1",
    api_ver_projects: str = "v1",
    api_ver_locations: str = "v1",
    api_ver_flavors: str = "v1",
    api_ver_images: str = "v1",
    api_ver_identity_providers: str = "v1",
    api_ver_services: str = "v1",
    api_ver_slas: str = "v1",
    api_ver_user_groups: str = "v1",
) -> None:
    """Add a new provider to the CMDB with the given attributes."""

    print(f"Adding provider {provider.name} to CMDB")

    provider_url = os.path.join(url, f"api/{api_ver_providers}/providers/")
    flavor_url = os.path.join(url, f"api/{api_ver_flavors}/flavors/")
    image_url = os.path.join(url, f"api/{api_ver_images}/images/")
    project_url = os.path.join(url, f"api/{api_ver_projects}/projects/")
    os.path.join(url, f"/api/{api_ver_locations}/locations/")

    resp = requests.get(
        url=provider_url,
        params={"name": provider.name, "with_conn": True},
        headers={"Authorization": f"Bearer {token}"},
    )
    if resp.status_code == status.HTTP_200_OK:
        provider_list = resp.json()

        if len(provider_list) == 0:
            print(f"No match found. Creating new provider '{provider.name}'")
            resp = requests.post(
                url=provider_url,
                json=jsonable_encoder(provider),
                headers={
                    "accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}",
                },
            )
            if resp.status_code == status.HTTP_201_CREATED:
                print(f"Provider '{provider.name}' created")
            else:
                print(f"Failed to create provider '{provider.name}'")
                print(f"Status code: {resp.status_code}")
                print(f"Message: {resp.text}")

        elif len(provider_list) == 1:
            print(
                f"Exactly one match found. Trying to update provider '{provider.name}'"
            )
            db_provider = ProviderRead(**provider_list[0])

            resp = requests.patch(
                url=os.path.join(provider_url, str(db_provider.uid)),
                json=jsonable_encoder(provider),
                headers={
                    "accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}",
                },
            )
            if resp.status_code == status.HTTP_200_OK:
                print(f"Provider '{provider.name}' successfully updated")
            elif resp.status_code == status.HTTP_304_NOT_MODIFIED:
                print("New data matches stored data.")
                print(f"Provider '{provider.name}' not modified")
            else:
                print(f"Failed to update provider '{provider.name}'")
                print(f"Status code: {resp.status_code}")
                print(f"Message: {resp.text}")

            for flavor in provider.flavors:
                db_flavor = None
                if flavor.name in [i.name for i in db_provider.flavors]:
                    idx = [i.name for i in db_provider.flavors].index(flavor.name)
                    db_flavor = db_provider.flavors[idx]
                    print(
                        f"A flavor with name '{flavor.name}' already belongs to "
                        f"provider '{provider.name}'"
                    )
                elif flavor.uuid in [i.uuid for i in db_provider.flavors]:
                    idx = [i.uuid for i in db_provider.flavors].index(flavor.uuid)
                    db_flavor = db_provider.flavors[idx]
                    print(
                        f"A flavor with uuid '{flavor.uuid}' already belongs to "
                        f"provider '{provider.name}'"
                    )
                else:
                    print(
                        f"No flavors with name '{flavor.name}' or uuid '{flavor.uuid}' "
                        f"belongs to provider {provider.name}'."
                    )

                if db_flavor is not None:
                    print(f"Trying to update flavor '{flavor.name}'.")
                    resp = requests.patch(
                        url=os.path.join(flavor_url, str(db_flavor.uid)),
                        json=jsonable_encoder(flavor),
                        headers={
                            "accept": "application/json",
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {token}",
                        },
                    )
                    if resp.status_code == status.HTTP_200_OK:
                        print(f"Flavor '{flavor.name}' successfully updated")
                    elif resp.status_code == status.HTTP_304_NOT_MODIFIED:
                        print("New data matches stored data.")
                        print(f"Flavor '{flavor.name}' not modified")
                    else:
                        print(f"Failed to update flavor'{flavor.name}'")
                        print(f"Status code: {resp.status_code}")
                        print(f"Message: {resp.text}")

                else:
                    print(f"Creating new flavor '{flavor.name}'.")
                    resp = requests.post(
                        url=os.path.join(provider_url, str(db_provider.uid), "flavors"),
                        json=jsonable_encoder(flavor),
                        headers={
                            "accept": "application/json",
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {token}",
                        },
                    )
                    if resp.status_code == status.HTTP_201_CREATED:
                        print(f"Flavor '{flavor.name}' successfully created")
                    elif resp.status_code == status.HTTP_400_BAD_REQUEST:
                        print(f"Flavor '{flavor.name}' already exists.")
                    else:
                        print(f"Failed to create flavor '{flavor.name}'")
                        print(f"Status code: {resp.status_code}")
                        print(f"Message: {resp.text}")

            for image in provider.images:
                db_image = None
                if image.name in [i.name for i in db_provider.images]:
                    idx = [i.name for i in db_provider.images].index(image.name)
                    db_image = db_provider.images[idx]
                    print(
                        f"A image with name '{image.name}' already belongs to "
                        f"provider '{provider.name}'"
                    )
                elif image.uuid in [i.uuid for i in db_provider.images]:
                    idx = [i.uuid for i in db_provider.images].index(image.uuid)
                    db_image = db_provider.images[idx]
                    print(
                        f"A image with uuid '{image.uuid}' already belongs to "
                        f"provider '{provider.name}'"
                    )
                else:
                    print(
                        f"No images with name '{image.name}' or uuid '{image.uuid}' "
                        f"belongs to provider {provider.name}'."
                    )

                if db_image is not None:
                    print(f"Trying to update image '{image.name}'.")
                    resp = requests.patch(
                        url=os.path.join(image_url, str(db_image.uid)),
                        json=jsonable_encoder(image),
                        headers={
                            "accept": "application/json",
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {token}",
                        },
                    )
                    if resp.status_code == status.HTTP_200_OK:
                        print(f"Image '{image.name}' successfully updated")
                    elif resp.status_code == status.HTTP_304_NOT_MODIFIED:
                        print("New data matches stored data.")
                        print(f"Image '{image.name}' not modified")
                    else:
                        print(f"Failed to update image'{image.name}'")
                        print(f"Status code: {resp.status_code}")
                        print(f"Message: {resp.text}")

                else:
                    print(f"Creating new image '{image.name}'.")
                    resp = requests.post(
                        url=os.path.join(provider_url, str(db_provider.uid), "images"),
                        json=jsonable_encoder(image),
                        headers={
                            "accept": "application/json",
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {token}",
                        },
                    )
                    if resp.status_code == status.HTTP_201_CREATED:
                        print(f"Image '{image.name}' successfully created")
                    elif resp.status_code == status.HTTP_400_BAD_REQUEST:
                        print(f"Image '{image.name}' already exists.")
                    else:
                        print(f"Failed to create image '{image.name}'")
                        print(f"Status code: {resp.status_code}")
                        print(f"Message: {resp.text}")

            for project in provider.projects:
                db_project = None
                if project.name in [i.name for i in db_provider.projects]:
                    idx = [i.name for i in db_provider.projects].index(project.name)
                    db_project = db_provider.projects[idx]
                    print(
                        f"A project with name '{project.name}' already belongs to "
                        f"provider '{provider.name}'"
                    )
                elif project.uuid in [i.uuid for i in db_provider.projects]:
                    idx = [i.uuid for i in db_provider.projects].index(project.uuid)
                    db_project = db_provider.projects[idx]
                    print(
                        f"A project with uuid '{project.uuid}' already belongs to "
                        f"provider '{provider.name}'"
                    )
                else:
                    print(
                        f"No projects with name '{project.name}' or uuid "
                        f"'{project.uuid}' belongs to provider {provider.name}'."
                    )

                if db_project is not None:
                    print(f"Trying to update project '{project.name}'.")
                    resp = requests.patch(
                        url=os.path.join(project_url, str(db_project.uid)),
                        json=jsonable_encoder(project),
                        headers={
                            "accept": "application/json",
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {token}",
                        },
                    )
                    if resp.status_code == status.HTTP_200_OK:
                        print(f"Project '{project.name}' successfully updated")
                    elif resp.status_code == status.HTTP_304_NOT_MODIFIED:
                        print("New data matches stored data.")
                        print(f"Project '{project.name}' not modified")
                    else:
                        print(f"Failed to update project'{project.name}'")
                        print(f"Status code: {resp.status_code}")
                        print(f"Message: {resp.text}")

                else:
                    print(f"Creating new project '{project.name}'.")
                    resp = requests.post(
                        url=os.path.join(
                            provider_url, str(db_provider.uid), "projects"
                        ),
                        json=jsonable_encoder(project),
                        headers={
                            "accept": "application/json",
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {token}",
                        },
                    )
                    if resp.status_code == status.HTTP_201_CREATED:
                        print(f"Project '{project.name}' successfully created")
                    elif resp.status_code == status.HTTP_400_BAD_REQUEST:
                        print(f"Project '{project.name}' already exists.")
                    else:
                        print(f"Failed to create project '{project.name}'")
                        print(f"Status code: {resp.status_code}")
                        print(f"Message: {resp.text}")

        # Multiple matches -> DB Corrupted
        else:
            print(f"Multiple providers with the same name '{provider.name}'")
