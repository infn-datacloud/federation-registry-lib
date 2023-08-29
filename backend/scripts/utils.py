from typing import List

from app.service.schemas import ServiceBase


def get_service_url(
    *, services: List[ServiceBase], srv_type: str, srv_name: str
) -> str:
    """From list of services return specific service endpoint."""

    for service in services:
        if service.type == srv_type and service.name == srv_name:
            return service.endpoint
    raise  # TODO
