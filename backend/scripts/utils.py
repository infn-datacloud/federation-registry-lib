import os
from typing import Dict, List, Tuple

import yaml
from crud import CRUD
from logger import logger
from models.cmdb import CMDB, URLs
from models.provider import SiteConfig

from app.provider.schemas_extended import ProviderCreateExtended


def load_cmdb_config(*, base_path: str = ".") -> SiteConfig:
    """Load CMDB configuration."""
    logger.info("Loading CMDB configuration")
    with open(os.path.join(base_path, ".cmdb-config.yaml")) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    config = CMDB(**config)
    logger.debug(f"{repr(config)}")

    d = {}
    for k, v in config.api_ver.dict().items():
        d[k] = os.path.join(config.base_url, "api", f"{v}", f"{k}")
    urls = URLs(**d)
    logger.debug(f"{repr(urls)}")
    return urls


def load_config(*, fname: str) -> SiteConfig:
    """Load provider configuration from yaml file."""
    logger.info(f"Loading provider configuration from {fname}")
    with open(fname) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        config = SiteConfig(**config)

    logger.info("Configuration loaded")
    logger.debug(f"{repr(config)}")
    return config


def get_read_write_headers(*, token: str) -> Tuple[Dict[str, str], Dict[str, str]]:
    """From an access token, create the read and write headers."""
    read_header = {"authorization": f"Bearer {token}"}
    write_header = {
        **read_header,
        "accept": "application/json",
        "content-type": "application/json",
    }
    return (read_header, write_header)


def update_database(
    *, cmdb_urls: URLs, items: List[ProviderCreateExtended], token: str
) -> None:
    """Use the read and write headers to create, update or remove providers from the
    CMDB.
    """
    read_header, write_header = get_read_write_headers(token=token)
    crud = CRUD(
        url=cmdb_urls.providers, read_headers=read_header, write_headers=write_header
    )

    logger.info("Retrieving data from CMDB")
    db_items = {db_item.name: db_item for db_item in crud.read(with_conn=True)}
    for item in items:
        db_item = db_items.pop(item.name, None)
        if db_item is None:
            crud.create(data=item)
        else:
            crud.update(new_data=item, old_data=db_item)
    for db_item in db_items.values():
        crud.remove(item=db_item)
