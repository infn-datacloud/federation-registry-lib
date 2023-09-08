import os
import subprocess
from typing import List

import yaml
from models.config import IDP, Config
from pydantic import AnyHttpUrl


def choose_idp(
    *, identity_providers: List[IDP], preferred_idp_list: List[AnyHttpUrl]
) -> IDP:
    for idp_url in preferred_idp_list:
        for chosen_idp in identity_providers:
            if idp_url == chosen_idp.endpoint:
                return chosen_idp


def generate_token(*, endpoint: AnyHttpUrl) -> str:
    token_cmd = subprocess.run(
        ["docker", "exec", "catalog-api-oidc-agent-1", "oidc-token", endpoint],
        stdout=subprocess.PIPE,
        text=True,
    )
    return token_cmd.stdout.strip("\n")


def load_config(*, base_path: str = ".", fname: str = "config.yaml") -> Config:
    with open(os.path.join(base_path, fname)) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return Config(**config)
