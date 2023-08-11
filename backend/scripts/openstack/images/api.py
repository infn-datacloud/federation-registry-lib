import os
import requests
from typing import List

from scripts.openstack.images.schemas import Image


def get_images(*, os_image_url: str, token: str) -> List[Image]:
    """Get list of images"""

    headers = {"X-Auth-Token": token}
    resp = requests.get(
        url=os.path.join(os_image_url, "/v2/images/"), headers=headers
    )
    if resp.status == 201:
        return resp.json().get("images")
    raise  # TODO
