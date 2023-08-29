from app.provider.schemas_extended import ProviderCreateExtended
from scripts.cmdb.api import add_provider
from scripts.openstack.auth.api import get_token
from scripts.openstack.flavors.api import get_flavors
from scripts.openstack.images.api import get_images
from scripts.openstack.projects.api import get_projects
from scripts.openstack.services.api import get_catalog, get_services
from scripts.openstack.services.utils import merge_services_and_catalog_info
from scripts.utils import get_service_url

if __name__ == "__main__":
    cmdb_url = "http://localhost:8000"

    provider_name = ""
    provider_desc = ""
    provider_is_public = False
    provider_contacts = []

    os_auth_url = ""

    # Authenticate in order to get token.
    os_username = ""
    os_password = ""
    token = get_token(
        os_auth_url=os_auth_url,
        os_username=os_username,
        os_password=os_password,
    )

    # From the identity service URL get the list of services.
    # Using the auth token retrieve the catalog list
    # and assign to each service the corresponding url.
    catalog = get_catalog(os_auth_url=os_auth_url, token=token)
    services = get_services(os_auth_url=os_auth_url, token=token)
    services = merge_services_and_catalog_info(
        services=services, catalog=catalog
    )

    # From the identity service URL get the list of projects
    projects = get_projects(os_auth_url=os_auth_url, token=token)

    # From the nova service URL get the list of flavors
    os_compute_url = get_service_url(
        services=services, srv_type="compute", srv_name="nova"
    )
    flavors = get_flavors(os_compute_url=os_compute_url, token=token)

    # From the image service URL get the list of images
    os_image_url = get_service_url(
        services=services, srv_type="image", srv_name="glance"
    )
    images = get_images(os_image_url=os_image_url, token=token)

    provider = ProviderCreateExtended(
        name=provider_name,
        description=provider_desc,
        is_public=provider_is_public,
        support_emails=provider_contacts,
        flavors=flavors,
        images=images,
        projects=projects,
        services=services,
    )
    db_provider = add_provider(cmdb_url=cmdb_url, provider=provider)
