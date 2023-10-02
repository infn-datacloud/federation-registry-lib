import os
from typing import Dict, Tuple

import yaml
from logger import logger
from models.config import CMDB, Config, Region, URLs


def load_cmdb_config(*, base_path: str = ".") -> Config:
    logger.info("Loading CMDB configuration")
    with open(os.path.join(base_path, ".cmdb-config.yaml")) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    config = CMDB(**config)
    d = {}
    for k, v in config.api_ver.dict().items():
        d[k] = os.path.join(config.base_url, "api", f"{v}", f"{k}")
    return URLs(**d)


def load_config(*, fname: str, cmdb_urls: CMDB) -> Config:
    logger.info("Loading configuration")

    with open(fname) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        config = Config(cmdb_urls=cmdb_urls, **config)
        for os_conf in config.openstack:
            if len(os_conf.regions) == 0:
                os_conf.regions.append(Region(name="RegionOne"))
        for k8s_conf in config.kubernetes:
            if len(k8s_conf.regions) == 0:
                k8s_conf.regions.append(Region(name="default"))

    logger.info("Configuration loaded")
    return config


def get_read_write_headers(*, token: str) -> Tuple[Dict[str, str], Dict[str, str]]:
    read_header = {"authorization": f"Bearer {token}"}
    write_header = {
        **read_header,
        "accept": "application/json",
        "content-type": "application/json",
    }
    return (read_header, write_header)
