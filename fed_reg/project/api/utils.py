"""Utilities used in Project endpoints."""


from fed_reg.project.models import Project
from fed_reg.region.schemas import RegionQuery


def filter_on_region_attr(  # noqa: C901
    items: list[Project], region_query: RegionQuery
) -> list[Project]:
    """Filter projects based on region access."""
    attrs = region_query.dict(exclude_none=True)
    if not attrs:
        return items

    for item in items:
        for quota in item.quotas:
            service = quota.service.single()
            if not service.regions.get_or_none(**attrs):
                item.quotas = item.quotas.exclude(uid=quota.uid)
        for flavor in item.private_flavors:
            service = flavor.service.single()
            if not service.regions.get_or_none(**attrs):
                item.private_flavors = item.private_flavors.exclude(uid=flavor.uid)
        for image in item.private_images:
            service = image.service.single()
            if not service.regions.get_or_none(**attrs):
                item.private_images = item.private_images.exclude(uid=image.uid)
        for network in item.private_networks:
            service = network.service.single()
            if not service.regions.get_or_none(**attrs):
                item.private_networks = item.private_networks.exclude(uid=network.uid)
    return items
