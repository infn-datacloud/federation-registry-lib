from pytest_cases import case, parametrize

from fedreg.flavor.models import PrivateFlavor, SharedFlavor
from fedreg.identity_provider.models import IdentityProvider
from fedreg.image.models import PrivateImage, SharedImage
from fedreg.network.models import PrivateNetwork, SharedNetwork
from fedreg.provider.models import Provider
from fedreg.quota.models import (
    BlockStorageQuota,
    ComputeQuota,
    NetworkQuota,
    ObjectStoreQuota,
)
from fedreg.region.models import Region
from fedreg.service.enum import ServiceType
from fedreg.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
    ObjectStoreService,
)
from fedreg.sla.models import SLA
from fedreg.user_group.models import UserGroup
from tests.models.utils import (
    auth_method_model_dict,
    flavor_model_dict,
    image_model_dict,
    network_model_dict,
    provider_model_dict,
    quota_model_dict,
    region_model_dict,
    service_model_dict,
)


class CaseAttr:
    @case(tags="sla")
    @parametrize(presence=(True, False))
    def case_slas(
        self,
        sla_model: SLA,
        user_group_model: UserGroup,
        identity_provider_model: IdentityProvider,
        provider_model: Provider,
        presence: bool,
    ) -> SLA | None:
        if presence:
            provider_model.identity_providers.connect(
                identity_provider_model, auth_method_model_dict()
            )
            identity_provider_model.user_groups.connect(user_group_model)
            user_group_model.slas.connect(sla_model)
            return sla_model
        return None

    @case(tags="flavors")
    @parametrize(prv_len=(0, 1, 2))
    @parametrize(sha_len=(0, 1, 2))
    def case_flavors(
        self,
        provider_model: Provider,
        region_model: Region,
        compute_service_model: ComputeService,
        compute_quota_model: ComputeQuota,
        prv_len: int,
        sha_len: int,
    ) -> tuple[list[PrivateFlavor], list[SharedFlavor]]:
        private_flavors = []
        shared_flavors = []
        provider_model.regions.connect(region_model)
        region_model.services.connect(compute_service_model)
        compute_service_model.quotas.connect(compute_quota_model)
        for _ in range(prv_len):
            flavor = PrivateFlavor(**flavor_model_dict()).save()
            compute_service_model.flavors.connect(flavor)
            private_flavors.append(flavor)
        for _ in range(sha_len):
            flavor = SharedFlavor(**flavor_model_dict()).save()
            compute_service_model.flavors.connect(flavor)
            shared_flavors.append(flavor)
        return private_flavors, shared_flavors

    @case(tags="images")
    @parametrize(prv_len=(0, 1, 2))
    @parametrize(sha_len=(0, 1, 2))
    def case_images(
        self,
        provider_model: Provider,
        region_model: Region,
        compute_service_model: ComputeService,
        compute_quota_model: ComputeQuota,
        prv_len: int,
        sha_len: int,
    ) -> tuple[list[PrivateImage], list[SharedImage]]:
        private_images = []
        shared_images = []
        provider_model.regions.connect(region_model)
        region_model.services.connect(compute_service_model)
        compute_service_model.quotas.connect(compute_quota_model)
        for _ in range(prv_len):
            image = PrivateImage(**image_model_dict()).save()
            compute_service_model.images.connect(image)
            private_images.append(image)
        for _ in range(sha_len):
            image = SharedImage(**image_model_dict()).save()
            compute_service_model.images.connect(image)
            shared_images.append(image)
        return private_images, shared_images

    @case(tags="networks")
    @parametrize(prv_len=(0, 1, 2))
    @parametrize(sha_len=(0, 1, 2))
    def case_networks(
        self,
        provider_model: Provider,
        region_model: Region,
        network_service_model: NetworkService,
        network_quota_model: NetworkQuota,
        prv_len: int,
        sha_len: int,
    ) -> tuple[list[PrivateNetwork], list[SharedNetwork]]:
        private_networks = []
        shared_networks = []
        provider_model.regions.connect(region_model)
        region_model.services.connect(network_service_model)
        network_service_model.quotas.connect(network_quota_model)
        for _ in range(prv_len):
            network = PrivateNetwork(**network_model_dict()).save()
            network_service_model.networks.connect(network)
            private_networks.append(network)
        for _ in range(sha_len):
            network = SharedNetwork(**network_model_dict()).save()
            network_service_model.networks.connect(network)
            shared_networks.append(network)
        return private_networks, shared_networks

    @case(tags="quotas")
    @parametrize(len=(0, 1, 2))
    def case_block_storage_quotas(
        self,
        provider_model: Provider,
        region_model: Region,
        block_storage_service_model: BlockStorageService,
        len: int,
    ) -> list[BlockStorageQuota]:
        provider_model.regions.connect(region_model)
        region_model.services.connect(block_storage_service_model)
        quotas = []
        for _ in range(len):
            quota = BlockStorageQuota(**quota_model_dict()).save()
            block_storage_service_model.quotas.connect(quota)
            quotas.append(quota)
        return quotas

    @case(tags="quotas")
    @parametrize(len=(0, 1, 2))
    def case_compute_quotas(
        self,
        provider_model: Provider,
        region_model: Region,
        compute_service_model: ComputeService,
        len: int,
    ) -> list[ComputeQuota]:
        provider_model.regions.connect(region_model)
        region_model.services.connect(compute_service_model)
        quotas = []
        for _ in range(len):
            quota = ComputeQuota(**quota_model_dict()).save()
            compute_service_model.quotas.connect(quota)
            quotas.append(quota)
        return quotas

    @case(tags="quotas")
    @parametrize(len=(0, 1, 2))
    def case_network_quotas(
        self,
        provider_model: Provider,
        region_model: Region,
        network_service_model: NetworkService,
        len: int,
    ) -> list[NetworkQuota]:
        provider_model.regions.connect(region_model)
        region_model.services.connect(network_service_model)
        quotas = []
        for _ in range(len):
            quota = NetworkQuota(**quota_model_dict()).save()
            network_service_model.quotas.connect(quota)
            quotas.append(quota)
        return quotas

    @case(tags="quotas")
    @parametrize(len=(0, 1, 2))
    def case_object_store_quotas(
        self,
        provider_model: Provider,
        region_model: Region,
        object_store_service_model: ObjectStoreService,
        len: int,
    ) -> list[ObjectStoreQuota]:
        provider_model.regions.connect(region_model)
        region_model.services.connect(object_store_service_model)
        quotas = []
        for _ in range(len):
            quota = ObjectStoreQuota(**quota_model_dict()).save()
            object_store_service_model.quotas.connect(quota)
            quotas.append(quota)
        return quotas

    @case(tags="quotas")
    def case_quotas(
        self,
        provider_model: Provider,
        region_model: Region,
        block_storage_service_model: BlockStorageService,
        compute_service_model: ComputeService,
        network_service_model: NetworkService,
        object_store_service_model: ObjectStoreService,
        block_storage_quota_model: BlockStorageQuota,
        compute_quota_model: ComputeQuota,
        network_quota_model: NetworkQuota,
        object_store_quota_model: ObjectStoreQuota,
    ) -> list[BlockStorageQuota | ComputeQuota | NetworkQuota | ObjectStoreQuota]:
        provider_model.regions.connect(region_model)
        region_model.services.connect(block_storage_service_model)
        block_storage_service_model.quotas.connect(block_storage_quota_model)
        region_model.services.connect(compute_service_model)
        compute_service_model.quotas.connect(compute_quota_model)
        region_model.services.connect(network_service_model)
        network_service_model.quotas.connect(network_quota_model)
        region_model.services.connect(object_store_service_model)
        object_store_service_model.quotas.connect(object_store_quota_model)
        return [
            block_storage_quota_model,
            compute_quota_model,
            network_quota_model,
            object_store_quota_model,
        ]

    @case(tags="providers")
    @parametrize(len=(1, 2))
    def case_providers(
        self, len: int
    ) -> tuple[list[PrivateNetwork], list[SharedNetwork]]:
        return [Provider(**provider_model_dict()).save() for _ in range(len)]

    @case(tags="network_kind")
    def case_private_network(
        self, private_network_model: PrivateNetwork
    ) -> PrivateNetwork:
        return private_network_model

    @case(tags="network_kind")
    def case_shared_network(self, shared_network_model: SharedNetwork) -> SharedNetwork:
        return shared_network_model

    @case(tags="regions")
    @parametrize(len=(0, 1, 2))
    def case_regions(self, len: int) -> list[Region]:
        return [Region(**region_model_dict()).save() for _ in range(len)]

    @case(tags="id_srv")
    @parametrize(len=(0, 1, 2))
    def case_identity_service(self, len: int) -> list[IdentityService]:
        return [
            IdentityService(**service_model_dict(ServiceType.IDENTITY)).save()
            for _ in range(len)
        ]
