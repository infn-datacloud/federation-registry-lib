from typing import Dict

from cruds.flavor import FlavorCRUD
from cruds.identity_provider import IdentityProviderCRUD
from cruds.image import ImageCRUD
from cruds.location import LocationCRUD
from cruds.project import ProjectCRUD
from cruds.provider import ProviderCRUD
from cruds.quota import QuotaCRUD
from cruds.service import ServiceCRUD
from models.config import URLs


class CRUDs:
    def __init__(
        self,
        cmdb_urls: URLs,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        self.flavors = FlavorCRUD(
            get_url=cmdb_urls.flavors,
            post_url=cmdb_urls.providers,
            patch_url=cmdb_urls.flavors,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.identity_providers = IdentityProviderCRUD(
            get_url=cmdb_urls.identity_providers,
            post_url=cmdb_urls.identity_providers,
            patch_url=cmdb_urls.identity_providers,
            connect_url=cmdb_urls.providers,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.images = ImageCRUD(
            get_url=cmdb_urls.images,
            post_url=cmdb_urls.providers,
            patch_url=cmdb_urls.images,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.locations = LocationCRUD(
            get_url=cmdb_urls.locations,
            post_url=cmdb_urls.locations,
            patch_url=cmdb_urls.locations,
            connect_url=cmdb_urls.providers,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.projects = ProjectCRUD(
            get_url=cmdb_urls.projects,
            post_url=cmdb_urls.providers,
            patch_url=cmdb_urls.projects,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.providers = ProviderCRUD(
            get_url=cmdb_urls.providers,
            post_url=cmdb_urls.providers,
            patch_url=cmdb_urls.providers,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.quotas = QuotaCRUD(
            get_url=cmdb_urls.quotas,
            post_url=cmdb_urls.quotas,
            patch_url=cmdb_urls.quotas,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.services = ServiceCRUD(
            get_url=cmdb_urls.services,
            post_url=cmdb_urls.providers,
            patch_url=cmdb_urls.services,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        # slas = None
        # user_groups = None
