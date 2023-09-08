import os
import subprocess
from typing import List

import yaml
from logger import logger
from models.cmdb import AuthMethodWrite, IdentityProviderWrite
from models.config import IDP, Config
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


def load_config(*, base_path: str = ".", fname: str = "config.yaml") -> Config:
    logger.info("Loading configuration")
    with open(os.path.join(base_path, fname)) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    logger.info("Configuration loaded")
    return Config(**config)
