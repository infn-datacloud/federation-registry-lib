import os
import subprocess
from typing import Dict, List, Tuple

import yaml
from logger import logger
from models.cmdb import AuthMethodWrite, IdentityProviderWrite
from models.config import IDP, Config, URLs
from pydantic import AnyHttpUrl


def get_identity_providers(
    idp_list: List[IDP],
) -> List[IdentityProviderWrite]:
    logger.info("Retrieve current project accessible images")
    identity_providers = []
    for idp in idp_list:
        identity_providers.append(
            IdentityProviderWrite(
                endpoint=idp.endpoint,
                group_claim=idp.group_claim,
                relationship=AuthMethodWrite(idp_name=idp.name, protocol=idp.protocol),
            )
        )
    return identity_providers


def choose_idp(
    *, identity_providers: List[IDP], preferred_idp_list: List[AnyHttpUrl]
) -> IDP:
    for idp_url in preferred_idp_list:
        for chosen_idp in identity_providers:
            if idp_url == chosen_idp.endpoint:
                logger.info(f"Chosen identity provider: {chosen_idp.endpoint}")
                return chosen_idp


def generate_token(*, endpoint: AnyHttpUrl) -> str:
    logger.info("Generating access token")
    token_cmd = subprocess.run(
        ["docker", "exec", "catalog-api-oidc-agent-1", "oidc-token", endpoint],
        stdout=subprocess.PIPE,
        text=True,
    )
    logger.info("Access token generated")
    return token_cmd.stdout.strip("\n")


def load_config(*, base_path: str = ".", fname: str = ".config.yaml") -> Config:
    logger.info("Loading configuration")
    with open(os.path.join(base_path, fname)) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    logger.info("Configuration loaded")
    return Config(**config)


def build_cmdb_urls(*, config: Config) -> URLs:
    return URLs(
        flavors=os.path.join(
            config.cmdb.base_url, f"api/{config.cmdb.api_ver.flavors}/flavors/"
        ),
        identity_providers=os.path.join(
            config.cmdb.base_url,
            f"api/{config.cmdb.api_ver.identity_providers}/identity_providers/",
        ),
        images=os.path.join(
            config.cmdb.base_url, f"api/{config.cmdb.api_ver.images}/images/"
        ),
        locations=os.path.join(
            config.cmdb.base_url, f"api/{config.cmdb.api_ver.locations}/locations/"
        ),
        projects=os.path.join(
            config.cmdb.base_url, f"api/{config.cmdb.api_ver.projects}/projects/"
        ),
        providers=os.path.join(
            config.cmdb.base_url, f"api/{config.cmdb.api_ver.providers}/providers/"
        ),
        quotas=os.path.join(
            config.cmdb.base_url, f"api/{config.cmdb.api_ver.quotas}/quotas"
        ),
        services=os.path.join(
            config.cmdb.base_url, f"api/{config.cmdb.api_ver.services}/services/"
        ),
        slas=os.path.join(
            config.cmdb.base_url, f"api/{config.cmdb.api_ver.slas}/slas/"
        ),
        user_groups=os.path.join(
            config.cmdb.base_url, f"api/{config.cmdb.api_ver.user_groups}/user_groups/"
        ),
    )


def get_read_write_headers(*, token: str) -> Tuple[Dict[str, str], Dict[str, str]]:
    read_header = {"authorization": f"Bearer {token}"}
    write_header = {
        **read_header,
        "accept": "application/json",
        "content-type": "application/json",
    }
    return (read_header, write_header)
