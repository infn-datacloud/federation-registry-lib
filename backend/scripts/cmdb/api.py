import os

import requests
from app.provider.schemas_extended import ProviderCreateExtended, ProviderReadExtended


def add_provider(
    *, cmdb_url: str, provider: ProviderCreateExtended
) -> ProviderReadExtended:
    """Add a new provider to the CMDB with the given attributes"""

    resp = requests.post(
        url=os.path.join(cmdb_url, "/api/v1/providers/"),
        data=provider,
    )
    if resp.status_code != 201:
        raise  # TODO
    return resp.json()
