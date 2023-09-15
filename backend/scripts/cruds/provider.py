import os
from typing import Dict

from cruds.core import BasicCRUD
from cruds.flavor import FlavorCRUD
from cruds.identity_provider import IdentityProviderCRUD
from cruds.image import ImageCRUD
from cruds.location import LocationCRUD
from cruds.project import ProjectCRUD
from cruds.quota import QuotaCRUD
from cruds.service import ServiceCRUD
from models.cmdb.project import ProjectQuery
from models.cmdb.provider import ProviderQuery, ProviderRead, ProviderWrite
from models.config import URLs


class ProviderCRUD(BasicCRUD[ProviderWrite, ProviderRead, ProviderQuery]):
    def __init__(
        self,
        cmdb_urls: URLs,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            read_schema=ProviderRead,
            write_schema=ProviderWrite,
            get_url=cmdb_urls.providers,
            post_url=cmdb_urls.providers,
            patch_url=os.path.join(cmdb_urls.providers, "{uid}"),
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.flavors = FlavorCRUD(
            get_url=cmdb_urls.flavors,
            post_url=os.path.join(cmdb_urls.providers, "{parent_uid}", "flavors"),
            patch_url=os.path.join(cmdb_urls.flavors, "{uid}"),
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.identity_providers = IdentityProviderCRUD(
            get_url=cmdb_urls.identity_providers,
            post_url=cmdb_urls.identity_providers,
            patch_url=os.path.join(cmdb_urls.identity_providers, "{uid}"),
            connect_url=os.path.join(
                cmdb_urls.providers, "{parent_uid}", "identity_providers", "{uid}"
            ),
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.images = ImageCRUD(
            get_url=cmdb_urls.images,
            post_url=os.path.join(cmdb_urls.providers, "{parent_uid}", "images"),
            patch_url=os.path.join(cmdb_urls.images, "{uid}"),
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.locations = LocationCRUD(
            get_url=cmdb_urls.locations,
            post_url=cmdb_urls.locations,
            patch_url=os.path.join(cmdb_urls.locations, "{uid}"),
            connect_url=os.path.join(
                cmdb_urls.providers, "{parent_uid}", "locations", "{uid}"
            ),
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.projects = ProjectCRUD(
            get_url=cmdb_urls.projects,
            post_url=os.path.join(cmdb_urls.providers, "{parent_uid}", "projects"),
            patch_url=os.path.join(cmdb_urls.projects, "{uid}"),
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.quotas = QuotaCRUD(
            get_url=cmdb_urls.quotas,
            post_url=cmdb_urls.quotas,
            patch_url=os.path.join(cmdb_urls.quotas, "{uid}"),
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.services = ServiceCRUD(
            get_url=cmdb_urls.services,
            post_url=os.path.join(cmdb_urls.providers, "{parent_uid}", "services"),
            patch_url=os.path.join(cmdb_urls.services, "{uid}"),
            read_headers=read_headers,
            write_headers=write_headers,
        )
        # self.slas = None
        # self.user_groups = None

    def create_or_update(self, *, item: ProviderWrite) -> ProviderRead:
        db_item = self.single(data=ProviderQuery(name=item.name), with_conn=True)
        if db_item is None:
            db_item = self.create(new_data=item)
        else:
            db_item = self.update(new_data=item, old_data=db_item)

            for flavor in item.flavors:
                self.flavors.create_or_update(item=flavor, parent=db_item)
            for image in item.images:
                self.images.create_or_update(item=image, parent=db_item)
            for service in item.services:
                db_service = self.services.create_or_update(
                    item=service, parent=db_item
                )
                for project in item.projects:
                    if db_service.type == "compute":
                        project.compute_quota.service = db_service.uid
                    if db_service.type == "block-storage":
                        project.block_storage_quota.service = db_service.uid
            for project in item.projects:
                db_project = self.projects.create_or_update(
                    item=project, parent=db_item
                )

                db_project = self.projects.single(
                    data=ProjectQuery(name=project.name), with_conn=True
                )
                for quota in [project.compute_quota, project.block_storage_quota]:
                    self.quotas.create_or_update(item=quota, parent=db_project)
            for identity_item in item.identity_providers:
                self.identity_providers.create_or_update(
                    item=identity_item, parent=db_item
                )
            if item.location is not None:
                self.locations.create_or_update(item=item.location, parent=db_item)
