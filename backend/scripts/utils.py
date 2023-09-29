import os
from typing import Dict, Tuple

import yaml
from logger import logger
from models.config import ConfigIn, ConfigOut, TrustedIDPOut, URLs


def load_config(*, base_path: str = ".", fname: str = ".config.yaml") -> ConfigOut:
    logger.info("Loading configuration")
    with open(os.path.join(base_path, fname)) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    conf = ConfigIn(**config)

    d = {}
    for k, v in conf.cmdb.api_ver.dict().items():
        d[k] = os.path.join(conf.cmdb.base_url, "api", f"{v}", f"{k}")
    urls = URLs(**d)
    idps = []
    for idp in conf.trusted_idps:
        idps.append(TrustedIDPOut(**idp.dict()))
    conf = ConfigOut(
        cmdb_urls=urls,
        trusted_idps=idps,
        openstack=conf.openstack,
        kubernetes=conf.kubernetes,
    )
    logger.info("Configuration loaded")
    return conf


def get_read_write_headers(*, token: str) -> Tuple[Dict[str, str], Dict[str, str]]:
    read_header = {"authorization": f"Bearer {token}"}
    write_header = {
        **read_header,
        "accept": "application/json",
        "content-type": "application/json",
    }
    return (read_header, write_header)
