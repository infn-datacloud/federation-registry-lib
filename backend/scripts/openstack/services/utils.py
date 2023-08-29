from typing import Dict, List

from scripts.openstack.services.schemas import Endpoints, Service


def merge_services_and_catalog_info(
    *, services: List[Service], catalog: Dict[str, Endpoints]
) -> List[Service]:
    """From catalog information enrich service data with public endpoint."""

    for service in services:
        service.endpoint = catalog.get(service.uuid).public_endpoint
    return services
