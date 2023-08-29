import os
from typing import Dict, List

import requests
from scripts.openstack.services.schemas import Endpoints, Service


def get_catalog(*, os_auth_url: str, token: str) -> Dict[str, Endpoints]:
    """Using the auth token, get the service catalog"""

    headers = {"X-Auth-Token": token}
    resp = requests.get(
        url=os.path.join(os_auth_url, "/v3/auth/catalog/"), headers=headers
    )
    if resp.status != 201:
        raise  # TODO

    catalog = {}
    for item in resp.json().get("catalog"):
        catalog[item["id"]] = {}
        for endpoint in item["endpoints"]:
            interface = endpoint["interface"]
            catalog[item["id"]][f"{interface}_endpoint"] = endpoint["url"]

    return catalog


def get_services(*, os_auth_url: str, token: str) -> List[Service]:
    """Get list of services"""

    headers = {"X-Auth-Token": token}
    resp = requests.get(
        url=os.path.join(os_auth_url, "/v3/services/"), headers=headers
    )
    if resp.status == 201:
        return resp.json().get("services")
    raise  # TODO
