from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from typing import List

from cruds.provider import ProviderCRUD
from models.cmdb.provider import ProviderWrite
from models.config import Openstack, TrustedIDP
from providers.opnstk import get_provider
from utils import get_read_write_headers, load_config

MAX_WORKERS = 5


def add_os_provider_to_list(
    os_conf: Openstack, trusted_idps: List[TrustedIDP], providers: List[ProviderWrite]
):
    provider = get_provider(os_conf=os_conf, trusted_idps=trusted_idps)
    with data_lock:
        providers.append(provider)


if __name__ == "__main__":
    config = load_config()

    providers = []
    data_lock = Lock()
    thread_pool = ThreadPoolExecutor(max_workers=MAX_WORKERS)

    for os_conf in config.openstack:
        thread_pool.submit(
            add_os_provider_to_list,
            os_conf=os_conf,
            trusted_idps=config.trusted_idps,
            providers=providers,
        )

    thread_pool.shutdown(wait=True)

    read_header, write_header = get_read_write_headers(
        token=config.trusted_idps[0].token
    )
    crud = ProviderCRUD(
        cmdb_urls=config.cmdb_urls, read_headers=read_header, write_headers=write_header
    )
    update_providers = crud.synchronize(items=providers)
