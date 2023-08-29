import os
from typing import List

import requests
from scripts.openstack.flavors.schemas import Flavor


def get_flavors(*, os_compute_url: str, token: str) -> List[Flavor]:
    """Get list of flavors."""

    headers = {"X-Auth-Token": token}
    resp = requests.get(
        url=os.path.join(os_compute_url, "/flavors/"), headers=headers
    )
    if resp.status == 201:
        return resp.json().get("flavors")
    raise  # TODO
