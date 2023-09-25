from cruds.provider import ProviderCRUD
from providers.opnstk import get_provider
from utils import get_read_write_headers, load_config

if __name__ == "__main__":
    config = load_config()

    tokens = {}
    providers = []
    for os_conf in config.openstack:
        provider = get_provider(os_conf=os_conf, trusted_idps=config.trusted_idps)
        providers.append(provider)

    # To update CMDB data, we use the last chosen token to generate
    # read and write headers.
    read_header, write_header = get_read_write_headers(
        # token=tokens[chosen_idp.endpoint]
    )
    crud = ProviderCRUD(
        cmdb_urls=config.cmdb_urls, read_headers=read_header, write_headers=write_header
    )
    update_providers = crud.synchronize(items=providers)
