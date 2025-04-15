from typing import Any, Literal

from pytest_cases import case

from fedreg.image.models import SharedImage
from fedreg.provider.models import Provider
from fedreg.region.models import Region
from fedreg.service.enum import ServiceType
from fedreg.service.models import ComputeService
from tests.models.utils import (
    image_model_dict,
    provider_model_dict,
    region_model_dict,
    service_model_dict,
)
from tests.utils import random_lower_string


class CaseProviderModel:
    @case(tags=("dict", "valid"))
    def case_mandatory(self) -> dict[str, Any]:
        return provider_model_dict()

    @case(tags=("dict", "valid"))
    def case_description(self) -> dict[str, Any]:
        return {
            **provider_model_dict(),
            "description": random_lower_string(),
        }

    @case(tags=("dict", "valid"))
    def case_status(self) -> dict[str, Any]:
        return {
            **provider_model_dict(),
            "status": random_lower_string(),
        }

    @case(tags=("dict", "valid"))
    def case_is_public(self) -> dict[str, Any]:
        return {
            **provider_model_dict(),
            "is_public": True,
        }

    @case(tags=("dict", "valid"))
    def case_support_emails(self) -> dict[str, Any]:
        return {
            **provider_model_dict(),
            "support_emails": [random_lower_string()],
        }

    @case(tags=("dict", "invalid"))
    def case_missing_name(self) -> tuple[dict[str, Any], Literal["name"]]:
        d = provider_model_dict()
        d.pop("name")
        return d, "name"

    @case(tags=("dict", "invalid"))
    def case_missing_type(self) -> tuple[dict[str, Any], Literal["type"]]:
        d = provider_model_dict()
        d.pop("type")
        return d, "type"


class CaseProviderImages:
    @case(tags="images")
    def case_one_image_one_region(self) -> tuple[Provider, int]:
        provider = Provider(**provider_model_dict()).save()
        region = Region(**region_model_dict()).save()
        service = ComputeService(
            **service_model_dict(srv_type=ServiceType.COMPUTE)
        ).save()
        image = SharedImage(**image_model_dict()).save()
        provider.regions.connect(region)
        region.services.connect(service)
        service.images.connect(image)
        return provider, 1

    @case(tags="images")
    def case_two_independent_images(self) -> tuple[Provider, int]:
        provider = Provider(**provider_model_dict()).save()
        region1 = Region(**region_model_dict()).save()
        region2 = Region(**region_model_dict()).save()
        service1 = ComputeService(
            **service_model_dict(srv_type=ServiceType.COMPUTE)
        ).save()
        service2 = ComputeService(
            **service_model_dict(srv_type=ServiceType.COMPUTE)
        ).save()
        image1 = SharedImage(**image_model_dict()).save()
        image2 = SharedImage(**image_model_dict()).save()
        provider.regions.connect(region1)
        provider.regions.connect(region2)
        region1.services.connect(service1)
        region2.services.connect(service2)
        service1.images.connect(image1)
        service2.images.connect(image2)
        return provider, 2

    @case(tags="images")
    def case_shared_image(self) -> tuple[Provider, int]:
        provider = Provider(**provider_model_dict()).save()
        region1 = Region(**region_model_dict()).save()
        region2 = Region(**region_model_dict()).save()
        service1 = ComputeService(
            **service_model_dict(srv_type=ServiceType.COMPUTE)
        ).save()
        service2 = ComputeService(
            **service_model_dict(srv_type=ServiceType.COMPUTE)
        ).save()
        image1 = SharedImage(**image_model_dict()).save()
        provider.regions.connect(region1)
        provider.regions.connect(region2)
        region1.services.connect(service1)
        region2.services.connect(service2)
        service1.images.connect(image1)
        service2.images.connect(image1)
        return provider, 1
