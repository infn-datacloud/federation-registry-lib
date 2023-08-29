import os
from typing import List

import requests
from scripts.openstack.projects.schemas import Project


def get_projects(*, os_auth_url: str, token: str) -> List[Project]:
    """Get list of projects."""

    headers = {"X-Auth-Token": token}
    resp = requests.get(
        url=os.path.join(os_auth_url, "/v3/projects/"), headers=headers
    )
    if resp.status == 201:
        return resp.json().get("projects")
    raise  # TODO
