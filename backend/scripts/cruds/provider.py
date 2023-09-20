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
from cruds.sla import SLACRUD
from cruds.user_group import UserGroupCRUD
from models.cmdb.flavor import FlavorQuery
from models.cmdb.identity_provider import IdentityProviderQuery
from models.cmdb.image import ImageQuery
from models.cmdb.project import ProjectQuery
from models.cmdb.provider import ProviderQuery, ProviderRead, ProviderWrite
from models.cmdb.service import ServiceQuery
from models.cmdb.user_group import UserGroupQuery
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
            connect_url=os.path.join(
                cmdb_urls.projects, "{parent_uid}", "flavors", "{uid}"
            ),
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
            connect_url=os.path.join(
                cmdb_urls.projects, "{parent_uid}", "images", "{uid}"
            ),
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
        self.slas = SLACRUD(
            get_url=cmdb_urls.slas,
            post_url=cmdb_urls.slas,
            patch_url=os.path.join(cmdb_urls.slas, "{uid}"),
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.user_groups = UserGroupCRUD(
            get_url=cmdb_urls.user_groups,
            post_url=os.path.join(
                cmdb_urls.identity_providers, "{parent_uid}", "user_groups"
            ),
            patch_url=os.path.join(cmdb_urls.user_groups, "{uid}"),
            read_headers=read_headers,
            write_headers=write_headers,
        )

    def create_or_update(self, *, item: ProviderWrite) -> ProviderRead:
        db_item = self.single(data=ProviderQuery(name=item.name), with_conn=True)
        if db_item is None:
            db_item = self.create(new_data=item)
        else:
            updated_item = self.update(new_data=item, uid=db_item.uid)
            db_item = db_item if updated_item is None else updated_item

            for service in item.services:
                db_item = self.services.create_or_update(item=service, parent=db_item)
            for project in item.projects:
                db_item = self.projects.create_or_update(item=project, parent=db_item)
            for flavor in item.flavors:
                db_item = self.flavors.create_or_update(item=flavor, parent=db_item)
            for image in item.images:
                db_item = self.images.create_or_update(item=image, parent=db_item)
            for identity_item in item.identity_providers:
                db_item = self.identity_providers.create_or_update(
                    item=identity_item, parent=db_item
                )
            if item.location is not None:
                db_item = self.locations.create_or_update(
                    item=item.location, parent=db_item
                )

        # Connect private flavors to corresponding projects
        for flavor in item.flavors:
            for project_uuid in flavor.projects:
                db_flavor, idx = self.flavors.find_in_list(
                    data=FlavorQuery(name=flavor.name), db_items=db_item.flavors
                )
                db_project, idx = self.projects.find_in_list(
                    data=ProjectQuery(uuid=project_uuid), db_items=db_item.projects
                )
                if db_project is not None:
                    self.flavors.connect(uid=db_flavor.uid, parent_uid=db_project.uid)

        # Connect private images to corresponding projects
        for image in item.images:
            for project_uuid in image.projects:
                db_image, idx = self.images.find_in_list(
                    data=ImageQuery(name=image.name), db_items=db_item.images
                )
                db_project, idx = self.projects.find_in_list(
                    data=ProjectQuery(uuid=project_uuid), db_items=db_item.projects
                )
                if db_project is not None:
                    self.images.connect(uid=db_image.uid, parent_uid=db_project.uid)

        for project in item.projects:
            # Create quotas and connect to corresponding projects.
            db_project, idx = self.projects.find_in_list(
                data=ProjectQuery(uuid=project.uuid), db_items=db_item.projects
            )
            for quota in project.quotas:
                db_service, idx = self.services.find_in_list(
                    data=ServiceQuery(endpoint=quota.service), db_items=db_item.services
                )
                db_project = self.quotas.create_or_update(
                    item=quota, project=db_project, service=db_service
                )

            # Create user groups
            db_identity_provider, idx = self.identity_providers.find_in_list(
                data=IdentityProviderQuery(
                    endpoint=project.sla.user_group.identity_provider
                ),
                db_items=db_item.identity_providers,
            )
            db_identity_provider = self.user_groups.create_or_update(
                item=project.sla.user_group, parent=db_identity_provider
            )

            # Create SLAs
            db_user_group, idx = self.user_groups.find_in_list(
                data=UserGroupQuery(name=project.sla.user_group.name),
                db_items=db_identity_provider.user_groups,
            )
            db_project = self.slas.create_or_update(
                item=project.sla, project=db_project, user_group=db_user_group
            )
