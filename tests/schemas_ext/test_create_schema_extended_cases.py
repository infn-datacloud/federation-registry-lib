from pytest_cases import case, parametrize

from fedreg.service.enum import ServiceType
from tests.schemas.utils import (
    auth_method_schema_dict,
    flavor_schema_dict,
    identity_provider_schema_dict,
    image_schema_dict,
    location_schema_dict,
    network_schema_dict,
    project_schema_dict,
    quota_schema_dict,
    region_schema_dict,
    service_schema_dict,
    sla_schema_dict,
    user_group_schema_dict,
)
from tests.utils import random_lower_string


class CaseAttr:
    @case(tags=("projects", "valid"))
    @parametrize(len=(1, 2))
    def case_projects(self, len: int) -> list[dict]:
        return [project_schema_dict() for _ in range(len)]

    @case(tags=("projects", "duplicate"))
    def case_projects_dup_name(self) -> list[dict]:
        p1 = project_schema_dict()
        p2 = project_schema_dict()
        p2["name"] = p1["name"]
        return [p1, p2]

    @case(tags=("projects", "duplicate"))
    def case_projects_dup_uuid(self) -> list[dict]:
        p1 = project_schema_dict()
        p2 = project_schema_dict()
        p2["uuid"] = p1["uuid"]
        return [p1, p2]

    @case(tags=("identity_providers", "valid"))
    @parametrize(len=(1, 2))
    def case_identity_providers(self, len: int) -> tuple[list[dict], list[str]]:
        idps = []
        projects = []
        for _ in range(len):
            project = random_lower_string()
            d = identity_provider_schema_dict()
            d["relationship"] = auth_method_schema_dict()
            d["user_groups"] = [
                {
                    **user_group_schema_dict(),
                    "sla": {**sla_schema_dict(), "project": project},
                }
            ]
            idps.append(d)
            projects.append(project)
        return idps, projects

    @case(tags=("identity_providers", "duplicate"))
    def case_identity_providers_dup_endpoint(self) -> tuple[list[dict], list[str]]:
        p1 = random_lower_string()
        p2 = random_lower_string()
        idp1 = identity_provider_schema_dict()
        idp1["relationship"] = auth_method_schema_dict()
        idp1["user_groups"] = [
            {
                **user_group_schema_dict(),
                "sla": {**sla_schema_dict(), "project": p1},
            }
        ]
        idp2 = identity_provider_schema_dict()
        idp2["relationship"] = auth_method_schema_dict()
        idp2["user_groups"] = [
            {
                **user_group_schema_dict(),
                "sla": {**sla_schema_dict(), "project": p2},
            }
        ]
        idp2["endpoint"] = idp1["endpoint"]
        return [idp1, idp2], [p1, p2]

    @case(tags=("identity_providers", "no-project"))
    def case_identity_providers_proj_not_in_prov(self) -> dict:
        d = identity_provider_schema_dict()
        d["relationship"] = auth_method_schema_dict()
        d["user_groups"] = [
            {
                **user_group_schema_dict(),
                "sla": {**sla_schema_dict(), "project": random_lower_string()},
            }
        ]
        return d

    @case(tags=("identity_providers", "slas"))
    def case_identity_providers_dup_slas(self) -> tuple[dict, list[str]]:
        d = identity_provider_schema_dict()
        d["relationship"] = auth_method_schema_dict()
        sla1 = sla_schema_dict()
        sla2 = sla_schema_dict()
        sla2["doc_uuid"] = sla1["doc_uuid"]
        p1 = random_lower_string()
        p2 = random_lower_string()
        d["user_groups"] = [
            {**user_group_schema_dict(), "sla": {**sla1, "project": p1}},
            {**user_group_schema_dict(), "sla": {**sla2, "project": p2}},
        ]
        return d, [p1, p2]

    @case(tags=("identity_providers", "projects"))
    def case_identity_providers_dup_projects(self) -> tuple[dict, list[str]]:
        d = identity_provider_schema_dict()
        d["relationship"] = auth_method_schema_dict()
        p1 = random_lower_string()
        p2 = random_lower_string()
        d["user_groups"] = [
            {**user_group_schema_dict(), "sla": {**sla_schema_dict(), "project": p1}},
            {**user_group_schema_dict(), "sla": {**sla_schema_dict(), "project": p1}},
        ]
        return d, [p1, p2]

    @case(tags=("identity_provider", "valid"))
    @parametrize(len=(1, 2))
    def case_identity_provider(self, len: int) -> dict:
        d = identity_provider_schema_dict()
        d["relationship"] = auth_method_schema_dict()
        d["user_groups"] = []
        for _ in range(len):
            d["user_groups"].append(
                {
                    **user_group_schema_dict(),
                    "sla": {**sla_schema_dict(), "project": random_lower_string()},
                }
            )
        return d

    @case(tags=("identity_provider", "valid"))
    def case_identity_providers_miss_user_group(self) -> dict:
        d = identity_provider_schema_dict()
        d["relationship"] = auth_method_schema_dict()
        return d

    @case(tags=("identity_provider", "valid"))
    def case_identity_providers_empty_list(self) -> dict:
        d = identity_provider_schema_dict()
        d["relationship"] = auth_method_schema_dict()
        d["user_groups"] = []
        return d

    @case(tags=("identity_provider", "valid"))
    def case_identity_providers_miss_rel(self) -> dict:
        d = identity_provider_schema_dict()
        d["user_groups"] = [
            {
                **user_group_schema_dict(),
                "sla": {**sla_schema_dict(), "project": random_lower_string()},
            }
        ]
        return d

    @case(tags=("identity_provider", "invalid"))
    def case_identity_providers_dup_user_groups(self) -> dict:
        d = identity_provider_schema_dict()
        d["relationship"] = auth_method_schema_dict()
        user_group1 = user_group_schema_dict()
        user_group2 = user_group_schema_dict()
        user_group2["name"] = user_group1["name"]
        d["user_groups"] = [
            {
                **user_group1,
                "sla": {**sla_schema_dict(), "project": random_lower_string()},
            },
            {
                **user_group2,
                "sla": {**sla_schema_dict(), "project": random_lower_string()},
            },
        ]
        return d

    @case(tags=("user_group", "valid"))
    def case_user_group(self) -> dict:
        d = user_group_schema_dict()
        d["sla"] = {**sla_schema_dict(), "project": random_lower_string()}
        return d

    @case(tags=("user_group", "valid"))
    def case_user_group_miss_sla(self) -> dict:
        return user_group_schema_dict()

    @case(tags=("sla", "valid"))
    def case_sla(self) -> dict:
        d = sla_schema_dict()
        d["project"] = random_lower_string()
        return d

    @case(tags=("sla", "invalid"))
    def case_sla_miss_proj(self) -> dict:
        return sla_schema_dict()

    @case(tags=("regions", "valid", "base"))
    @parametrize(len=(1, 2))
    def case_regions(self, len: int) -> list[dict]:
        return [region_schema_dict() for _ in range(len)]

    @case(tags=("regions", "valid", "base"))
    def case_regions_flavor(self) -> list[dict]:
        d = region_schema_dict()
        d["compute_services"] = [
            {
                **service_schema_dict(ServiceType.COMPUTE),
                "flavors": [{**flavor_schema_dict()}],
            }
        ]
        return [d]

    @case(tags=("regions", "valid", "base"))
    def case_regions_image(self) -> list[dict]:
        d = region_schema_dict()
        d["compute_services"] = [
            {
                **service_schema_dict(ServiceType.COMPUTE),
                "images": [{**image_schema_dict()}],
            }
        ]
        return [d]

    @case(tags=("regions", "valid", "base"))
    def case_regions_network(self) -> list[dict]:
        d = region_schema_dict()
        d["network_services"] = [
            {
                **service_schema_dict(ServiceType.NETWORK),
                "networks": [{**network_schema_dict()}],
            }
        ]
        return [d]

    @case(tags=("regions", "valid", "project"))
    def case_regions_block_storage_quota_with_proj(self) -> tuple[dict, str]:
        p = random_lower_string()
        d = region_schema_dict()
        d["block_storage_services"] = [
            {
                **service_schema_dict(ServiceType.BLOCK_STORAGE),
                "quotas": [{**quota_schema_dict(), "project": p}],
            }
        ]
        return d, p

    @case(tags=("regions", "valid", "project"))
    def case_regions_compute_quota_with_proj(self) -> tuple[dict, str]:
        p = random_lower_string()
        d = region_schema_dict()
        d["compute_services"] = [
            {
                **service_schema_dict(ServiceType.COMPUTE),
                "quotas": [{**quota_schema_dict(), "project": p}],
            }
        ]
        return d, p

    @case(tags=("regions", "valid", "project"))
    def case_regions_network_quota_with_proj(self) -> tuple[dict, str]:
        p = random_lower_string()
        d = region_schema_dict()
        d["network_services"] = [
            {
                **service_schema_dict(ServiceType.NETWORK),
                "quotas": [{**quota_schema_dict(), "project": p}],
            }
        ]
        return d, p

    @case(tags=("regions", "valid", "project"))
    def case_regions_object_store_quota_with_proj(self) -> tuple[dict, str]:
        p = random_lower_string()
        d = region_schema_dict()
        d["object_store_services"] = [
            {
                **service_schema_dict(ServiceType.OBJECT_STORE),
                "quotas": [{**quota_schema_dict(), "project": p}],
            }
        ]
        return d, p

    @case(tags=("regions", "valid", "project"))
    def case_regions_flavor_with_proj(self) -> tuple[dict, str]:
        p = random_lower_string()
        d = region_schema_dict()
        d["compute_services"] = [
            {
                **service_schema_dict(ServiceType.COMPUTE),
                "flavors": [{**flavor_schema_dict(), "projects": [p]}],
            }
        ]
        return d, p

    @case(tags=("regions", "valid", "project"))
    def case_regions_image_with_proj(self) -> tuple[dict, str]:
        p = random_lower_string()
        d = region_schema_dict()
        d["compute_services"] = [
            {
                **service_schema_dict(ServiceType.COMPUTE),
                "images": [{**image_schema_dict(), "projects": [p]}],
            }
        ]
        return d, p

    @case(tags=("regions", "valid", "project"))
    def case_regions_network_with_proj(self) -> tuple[dict, str]:
        p = random_lower_string()
        d = region_schema_dict()
        d["network_services"] = [
            {
                **service_schema_dict(ServiceType.NETWORK),
                "networks": [{**network_schema_dict(), "projects": [p]}],
            }
        ]
        return d, p

    @case(tags=("regions", "duplicate"))
    def case_regions_dup_name(self) -> list[dict]:
        r1 = region_schema_dict()
        r2 = region_schema_dict()
        r2["name"] = r1["name"]
        return [r1, r2]

    @case(tags=("regions", "no-project"))
    def case_regions_block_storage_quota_proj_not_in_prov(self) -> dict:
        d = region_schema_dict()
        d["block_storage_services"] = [
            {
                **service_schema_dict(ServiceType.BLOCK_STORAGE),
                "quotas": [{**quota_schema_dict(), "project": random_lower_string()}],
            }
        ]
        return d

    @case(tags=("regions", "no-project"))
    def case_regions_compute_quota_proj_not_in_prov(self) -> dict:
        d = region_schema_dict()
        d["compute_services"] = [
            {
                **service_schema_dict(ServiceType.COMPUTE),
                "quotas": [{**quota_schema_dict(), "project": random_lower_string()}],
            }
        ]
        return d

    @case(tags=("regions", "no-project"))
    def case_regions_network_quota_proj_not_in_prov(self) -> dict:
        d = region_schema_dict()
        d["network_services"] = [
            {
                **service_schema_dict(ServiceType.NETWORK),
                "quotas": [{**quota_schema_dict(), "project": random_lower_string()}],
            }
        ]
        return d

    @case(tags=("regions", "no-project"))
    def case_regions_object_store_quota_store_proj_not_in_prov(self) -> dict:
        d = region_schema_dict()
        d["object_store_services"] = [
            {
                **service_schema_dict(ServiceType.OBJECT_STORE),
                "quotas": [{**quota_schema_dict(), "project": random_lower_string()}],
            }
        ]
        return d

    @case(tags=("regions", "no-project"))
    def case_regions_flavor_proj_not_in_prov(self) -> dict:
        d = region_schema_dict()
        d["compute_services"] = [
            {
                **service_schema_dict(ServiceType.COMPUTE),
                "flavors": [
                    {**flavor_schema_dict(), "projects": [random_lower_string()]}
                ],
            }
        ]
        return d

    @case(tags=("regions", "no-project"))
    def case_regions_image_proj_not_in_prov(self) -> dict:
        d = region_schema_dict()
        d["compute_services"] = [
            {
                **service_schema_dict(ServiceType.COMPUTE),
                "images": [
                    {**image_schema_dict(), "projects": [random_lower_string()]}
                ],
            }
        ]
        return d

    @case(tags=("regions", "no-project"))
    def case_regions_network_proj_not_in_prov(self) -> dict:
        d = region_schema_dict()
        d["network_services"] = [
            {
                **service_schema_dict(ServiceType.NETWORK),
                "networks": [
                    {**network_schema_dict(), "projects": [random_lower_string()]}
                ],
            }
        ]
        return d

    @case(tags=("region", "location"))
    @parametrize(presence=(True, False))
    def case_location(self, presence: bool) -> dict | None:
        return location_schema_dict() if presence else None

    @case(tags=("region", "services", "block-storage", "valid"))
    @parametrize(len=(0, 1, 2))
    def case_block_storage_services(self, len: int) -> list[dict]:
        return [service_schema_dict(ServiceType.BLOCK_STORAGE) for _ in range(len)]

    @case(tags=("region", "services", "compute", "valid"))
    @parametrize(len=(0, 1, 2))
    def case_compute_services(self, len: int) -> list[dict]:
        return [service_schema_dict(ServiceType.COMPUTE) for _ in range(len)]

    @case(tags=("region", "services", "identity", "valid"))
    @parametrize(len=(0, 1, 2))
    def case_idnetity_services(self, len: int) -> list[dict]:
        return [service_schema_dict(ServiceType.IDENTITY) for _ in range(len)]

    @case(tags=("region", "services", "network", "valid"))
    @parametrize(len=(0, 1, 2))
    def case_network_services(self, len: int) -> list[dict]:
        return [service_schema_dict(ServiceType.NETWORK) for _ in range(len)]

    @case(tags=("region", "services", "object-store", "valid"))
    @parametrize(len=(0, 1, 2))
    def case_objcet_store_services(self, len: int) -> list[dict]:
        return [service_schema_dict(ServiceType.OBJECT_STORE) for _ in range(len)]

    @case(tags=("region", "services", "block-storage", "invalid"))
    def case_block_storage_services_dup_endpoint(self) -> list[dict]:
        s1 = service_schema_dict(ServiceType.BLOCK_STORAGE)
        s2 = service_schema_dict(ServiceType.BLOCK_STORAGE)
        s2["endpoint"] = s1["endpoint"]
        return [s1, s2]

    @case(tags=("region", "services", "compute", "invalid"))
    def case_compute_services_dup_endpoint(self) -> list[dict]:
        s1 = service_schema_dict(ServiceType.COMPUTE)
        s2 = service_schema_dict(ServiceType.COMPUTE)
        s2["endpoint"] = s1["endpoint"]
        return [s1, s2]

    @case(tags=("region", "services", "identity", "invalid"))
    def case_idnetity_services_dup_endpoint(self) -> list[dict]:
        s1 = service_schema_dict(ServiceType.IDENTITY)
        s2 = service_schema_dict(ServiceType.IDENTITY)
        s2["endpoint"] = s1["endpoint"]
        return [s1, s2]

    @case(tags=("region", "services", "network", "invalid"))
    def case_network_services_dup_endpoint(self) -> list[dict]:
        s1 = service_schema_dict(ServiceType.NETWORK)
        s2 = service_schema_dict(ServiceType.NETWORK)
        s2["endpoint"] = s1["endpoint"]
        return [s1, s2]

    @case(tags=("region", "services", "object-store", "invalid"))
    def case_objcet_store_services_dup_endpoint(self) -> list[dict]:
        s1 = service_schema_dict(ServiceType.OBJECT_STORE)
        s2 = service_schema_dict(ServiceType.OBJECT_STORE)
        s2["endpoint"] = s1["endpoint"]
        return [s1, s2]

    @case(
        tags=(
            "service",
            "block-storage",
            "compute",
            "network",
            "object-store",
            "quotas",
        )
    )
    @parametrize(len=(1, 2))
    def case_quotas(self, len: int) -> list[dict]:
        return [
            {**quota_schema_dict(), "project": random_lower_string()}
            for _ in range(len)
        ]

    @case(tags=("service", "invalid"))
    def case_dup_quota(self) -> list[dict]:
        project = random_lower_string()
        q1 = quota_schema_dict()
        q2 = quota_schema_dict()
        q1["project"] = project
        q2["project"] = project
        return [q1, q2]

    @case(tags=("service", "invalid"))
    def case_dup_per_user_quota(self) -> list[dict]:
        project = random_lower_string()
        q1 = quota_schema_dict()
        q2 = quota_schema_dict()
        q1["per_user"] = True
        q1["project"] = project
        q2["per_user"] = True
        q2["project"] = project
        return [q1, q2]

    @case(tags=("service", "invalid"))
    def case_dup_usage_quota(self) -> list[dict]:
        project = random_lower_string()
        q1 = quota_schema_dict()
        q2 = quota_schema_dict()
        q1["usage"] = True
        q1["project"] = project
        q2["usage"] = True
        q2["project"] = project
        return [q1, q2]

    @case(tags=("service", "compute", "flavors"))
    @parametrize(len=(1, 2))
    def case_private_flavors(self, len: int) -> list[dict]:
        return [
            {**flavor_schema_dict(), "projects": [random_lower_string()]}
            for _ in range(len)
        ]

    @case(tags=("service", "compute", "flavors"))
    @parametrize(len=(1, 2))
    def case_shared_flavors(self, len: int) -> list[dict]:
        return [flavor_schema_dict() for _ in range(len)]

    @case(tags=("service", "compute", "flavors"))
    def case_flavors(self) -> list[dict]:
        private = {**flavor_schema_dict(), "projects": [random_lower_string()]}
        shared = flavor_schema_dict()
        return [private, shared]

    @case(tags=("service", "compute", "images"))
    @parametrize(len=(1, 2))
    def case_private_images(self, len: int) -> list[dict]:
        return [
            {**image_schema_dict(), "projects": [random_lower_string()]}
            for _ in range(len)
        ]

    @case(tags=("service", "compute", "images"))
    @parametrize(len=(1, 2))
    def case_shared_images(self, len: int) -> list[dict]:
        return [image_schema_dict() for _ in range(len)]

    @case(tags=("service", "compute", "images"))
    def case_images(self) -> list[dict]:
        private = {**image_schema_dict(), "projects": [random_lower_string()]}
        shared = image_schema_dict()
        return [private, shared]

    @case(tags=("service", "network", "networks"))
    @parametrize(len=(1, 2))
    def case_private_networks(self, len: int) -> list[dict]:
        return [
            {**network_schema_dict(), "projects": [random_lower_string()]}
            for _ in range(len)
        ]

    @case(tags=("service", "network", "networks"))
    @parametrize(len=(1, 2))
    def case_shared_networks(self, len: int) -> list[dict]:
        return [network_schema_dict() for _ in range(len)]

    @case(tags=("service", "network", "networks"))
    def case_networks(self) -> list[dict]:
        private = {**network_schema_dict(), "projects": [random_lower_string()]}
        shared = network_schema_dict()
        return [private, shared]

    @case(tags=("flavor", "image", "network", "projects"))
    @parametrize(len=(1, 2))
    def case_flavor_projects(self, len: int) -> list[dict]:
        return [random_lower_string() for _ in range(len)]
