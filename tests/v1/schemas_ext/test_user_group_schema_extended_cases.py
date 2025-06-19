from pytest_cases import case, parametrize

from fedreg.project.models import Project
from fedreg.provider.models import Provider
from fedreg.quota.models import (
    BlockStorageQuota,
    ComputeQuota,
    NetworkQuota,
    ObjectStoreQuota,
)
from fedreg.region.models import Region
from fedreg.service.models import (
    BlockStorageService,
    ComputeService,
    NetworkService,
    ObjectStoreService,
)
from fedreg.sla.models import SLA
from tests.v1.models.utils import (
    project_model_dict,
    provider_model_dict,
    quota_model_dict,
    sla_model_dict,
)


class CaseAttr:
    @case(tags="slas")
    @parametrize(len=(0, 1, 2))
    def case_slas(self, len: int) -> list[SLA]:
        slas = []
        for _ in range(len):
            sla = SLA(**sla_model_dict()).save()
            project = Project(**project_model_dict()).save()
            provider = Provider(**provider_model_dict()).save()
            sla.projects.connect(project)
            project.provider.connect(provider)
            slas.append(sla)
        return slas

    @case(tags="projects")
    @parametrize(len=(1, 2))
    def case_projects(self, len: int) -> list[Project]:
        projects = []
        for _ in range(len):
            project = Project(**project_model_dict()).save()
            provider = Provider(**provider_model_dict()).save()
            project.provider.connect(provider)
            projects.append(project)
        return projects

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
