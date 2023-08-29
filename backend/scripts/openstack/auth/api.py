import os

import requests


def get_token(*, os_auth_url: str, os_username: str, os_password: str) -> str:
    """Get token with Password authentication with unscoped authorization."""

    headers = {"Content-Type": "application/json"}
    data = {
        "auth": {
            "identity": {
                "methods": ["password"],
                "password": {
                    "user": {
                        "name": os_username,
                        "password": os_password,
                        "domain": {"name": "Default"},
                    }
                },
            }
        }
    }
    resp = requests.post(
        url=os.path.join(os_auth_url, "/v3/auth/tokens"),
        headers=headers,
        data=data,
    )
    if resp.status == 201:
        return resp.headers.get("X-Subject-Token")
    raise  # TODO
