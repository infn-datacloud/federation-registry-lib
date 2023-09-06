import sys
from pathlib import Path
from typing import List

from models import IDP
from pydantic import AnyHttpUrl

external_path = Path.cwd().parent
sys.path.insert(1, str(external_path))

from app.auth_method.schemas import AuthMethodCreate
from app.provider.schemas_extended import IdentityProviderCreateExtended

PREFERRED_IDP_LIST = ["https://iam.cloud.infn.it/"]


def get_identity_providers_from_config(
    idp_list: List[IDP],
) -> List[IdentityProviderCreateExtended]:
    identity_providers = []
    for idp in idp_list:
        identity_providers.append(
            IdentityProviderCreateExtended(
                endpoint=idp.endpoint,
                group_claim=idp.group_claim,
                relationship=AuthMethodCreate(idp_name=idp.name, protocol=idp.protocol),
            )
        )
    return identity_providers


def choose_idp(
    identity_providers: List[IdentityProviderCreateExtended],
) -> IdentityProviderCreateExtended:
    for idp_url in PREFERRED_IDP_LIST:
        for chosen_idp in identity_providers:
            if idp_url == chosen_idp.endpoint:
                return chosen_idp


def generate_token(endpoint: AnyHttpUrl) -> str:
    return None
