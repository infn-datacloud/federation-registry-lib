"""Provider specific fixtures."""
from typing import Any, Dict, List
from uuid import uuid4

import pytest
from pytest_cases import fixture, fixture_ref, fixture_union, parametrize

from app.provider.schemas_extended import (
    AuthMethodCreate,
    BlockStorageServiceCreateExtended,
    ComputeServiceCreateExtended,
    FlavorCreateExtended,
    IdentityProviderCreateExtended,
    ImageCreateExtended,
    NetworkCreateExtended,
    NetworkServiceCreateExtended,
    ProjectCreate,
    RegionCreateExtended,
    SLACreateExtended,
    UserGroupCreateExtended,
)
from tests.utils.provider import random_status, random_type
from tests.utils.utils import (
    random_bool,
    random_email,
    random_lower_string,
    random_start_end_dates,
    random_url,
)

invalid_create_key_values = [
    ("description", None),
    ("name", None),
    ("type", None),
    ("type", random_lower_string()),
    ("status", None),
    ("status", random_lower_string()),
    ("is_public", None),
]
relationships_num = [1, 2]
relationships_attr = ["identity_providers", "projects", "regions"]


@fixture
def provider_create_mandatory_data() -> Dict[str, Any]:
    """Dict with Provider mandatory attributes."""
    return {"name": random_lower_string(), "type": random_type()}


@fixture
def provider_create_all_data(
    provider_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all Provider attributes."""
    return {
        **provider_create_mandatory_data,
        "description": random_lower_string(),
        "status": random_status(),
        "is_public": random_bool(),
        "support_emails": [random_email()],
    }


@fixture
@parametrize(attr=relationships_attr)
def provider_create_data_passing_empty_list(
    attr: str, provider_create_all_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Dict with all Provider attributes.

    Passing an empty list is not a problem.
    """
    return {**provider_create_all_data, attr: []}


@fixture
@parametrize(owned_regions=relationships_num)
def provider_create_data_with_regions(
    owned_regions: int,
    provider_create_all_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all Provider attributes and regions."""
    regions = []
    for _ in range(owned_regions):
        regions.append(RegionCreateExtended(name=random_lower_string()))
    return {**provider_create_all_data, "regions": regions}


@fixture
@parametrize(owned_projects=relationships_num)
def provider_create_data_with_projects(
    owned_projects: int,
    provider_create_all_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all Provider attributes and regions."""
    projects = []
    for _ in range(owned_projects):
        projects.append(ProjectCreate(name=random_lower_string(), uuid=uuid4()))
    return {**provider_create_all_data, "projects": projects}


@fixture
def provider_create_data_with_idps(
    provider_create_data_with_projects: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all Provider attributes and regions."""
    projects: List[ProjectCreate] = provider_create_data_with_projects.get("projects")
    identity_providers = []
    for i in range(len(projects)):
        start_date, end_date = random_start_end_dates()
        identity_providers.append(
            IdentityProviderCreateExtended(
                endpoint=random_url(),
                group_claim=random_lower_string(),
                relationship=AuthMethodCreate(
                    idp_name=random_lower_string(), protocol=random_lower_string()
                ),
                user_groups=[
                    UserGroupCreateExtended(
                        name=random_lower_string(),
                        sla=SLACreateExtended(
                            doc_uuid=uuid4(),
                            start_date=start_date,
                            end_date=end_date,
                            project=projects[i].uuid,
                        ),
                    )
                ],
            )
        )
    return {
        **provider_create_data_with_projects,
        "identity_providers": identity_providers,
    }


@fixture
@parametrize("k, v", invalid_create_key_values)
def provider_create_invalid_pair(
    provider_create_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    data = {**provider_create_mandatory_data}
    data[k] = v
    return data


@fixture
def provider_create_duplicate_regions(
    provider_create_all_data: Dict[str, Any],
    region_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all Provider attributes and regions."""
    region = RegionCreateExtended(**region_create_mandatory_data)
    return {**provider_create_all_data, "regions": [region, region]}


@fixture
def provider_create_duplicate_projects(
    provider_create_all_data: Dict[str, Any],
    project_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all Provider attributes and regions."""
    project = ProjectCreate(**project_create_mandatory_data)
    return {**provider_create_all_data, "projects": [project, project]}


@fixture
def provider_create_duplicate_idps(
    provider_create_all_data: Dict[str, Any],
    identity_provider_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all Provider attributes and regions."""
    projects = [
        ProjectCreate(name=random_lower_string(), uuid=uuid4()),
        ProjectCreate(name=random_lower_string(), uuid=uuid4()),
    ]
    identity_providers = []
    for i in range(len(projects)):
        start_date, end_date = random_start_end_dates()
        identity_providers.append(
            IdentityProviderCreateExtended(
                **identity_provider_create_mandatory_data,
                relationship=AuthMethodCreate(
                    idp_name=random_lower_string(), protocol=random_lower_string()
                ),
                user_groups=[
                    UserGroupCreateExtended(
                        name=random_lower_string(),
                        sla=SLACreateExtended(
                            doc_uuid=uuid4(),
                            start_date=start_date,
                            end_date=end_date,
                            project=projects[i].uuid,
                        ),
                    )
                ],
            )
        )
    return {
        **provider_create_all_data,
        "projects": projects,
        "identity_providers": identity_providers,
    }


@fixture
def provider_create_duplicate_sla_same_user_group(
    provider_create_all_data: Dict[str, Any],
    identity_provider_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all Provider attributes and regions."""
    projects = [
        ProjectCreate(name=random_lower_string(), uuid=uuid4()),
        ProjectCreate(name=random_lower_string(), uuid=uuid4()),
    ]
    identity_providers = []
    sla_uuid = uuid4()
    for i in range(len(projects)):
        start_date, end_date = random_start_end_dates()
        identity_providers.append(
            IdentityProviderCreateExtended(
                **identity_provider_create_mandatory_data,
                relationship=AuthMethodCreate(
                    idp_name=random_lower_string(), protocol=random_lower_string()
                ),
                user_groups=[
                    UserGroupCreateExtended(
                        name=random_lower_string(),
                        sla=SLACreateExtended(
                            doc_uuid=sla_uuid,
                            start_date=start_date,
                            end_date=end_date,
                            project=projects[i].uuid,
                        ),
                    )
                ],
            )
        )
    return {
        **provider_create_all_data,
        "projects": projects,
        "identity_providers": identity_providers,
    }


@fixture
def provider_create_invalid_sla_project_uuid(
    provider_create_all_data: Dict[str, Any],
    identity_provider_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all Provider attributes and regions."""
    identity_provider = IdentityProviderCreateExtended(
        **identity_provider_create_data_with_rel
    )
    return {**provider_create_all_data, "identity_providers": [identity_provider]}


@fixture
def provider_create_invalid_block_storage_serv_project_uuid(
    provider_create_all_data: Dict[str, Any],
    region_create_mandatory_data: Dict[str, Any],
    block_storage_service_create_data_with_quotas: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all Provider attributes and regions."""
    region = RegionCreateExtended(
        **region_create_mandatory_data,
        block_storage_services=[
            BlockStorageServiceCreateExtended(
                **block_storage_service_create_data_with_quotas
            )
        ],
    )
    return {**provider_create_all_data, "regions": [region]}


@fixture
@parametrize(
    service_with_rel=(
        fixture_ref("compute_service_create_data_with_flavors"),
        fixture_ref("compute_service_create_data_with_images"),
        fixture_ref("compute_service_create_data_with_quotas"),
    ),
    idstyle="explicit",
)
def provider_create_invalid_compute_serv_project_uuid(
    provider_create_all_data: Dict[str, Any],
    region_create_mandatory_data: Dict[str, Any],
    service_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all Provider attributes and regions."""
    flavors: List[FlavorCreateExtended] = service_with_rel.get("flavors", [])
    if len(flavors) > 0 and flavors[0].is_public:
        pytest.skip("Public flavor does not have project UUIDs.")
    images: List[ImageCreateExtended] = service_with_rel.get("images", [])
    if len(images) > 0 and images[0].is_public:
        pytest.skip("Public image does not have project UUIDs.")
    region = RegionCreateExtended(
        **region_create_mandatory_data,
        compute_services=[ComputeServiceCreateExtended(**service_with_rel)],
    )
    return {**provider_create_all_data, "regions": [region]}


@fixture
@parametrize(
    service_with_rel=(
        fixture_ref("network_service_create_data_with_networks"),
        fixture_ref("network_service_create_data_with_quotas"),
    ),
    idstyle="explicit",
)
def provider_create_invalid_network_serv_project_uuid(
    provider_create_all_data: Dict[str, Any],
    region_create_mandatory_data: Dict[str, Any],
    service_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all Provider attributes and regions."""
    networks: List[NetworkCreateExtended] = service_with_rel.get("networks", [])
    if len(networks) > 0 and networks[0].is_shared:
        pytest.skip("Public network does not have project UUIDs.")
    region = RegionCreateExtended(
        **region_create_mandatory_data,
        network_services=[NetworkServiceCreateExtended(**service_with_rel)],
    )
    return {**provider_create_all_data, "regions": [region]}


provider_create_valid_data = fixture_union(
    "provider_create_valid_data",
    (
        provider_create_mandatory_data,
        provider_create_data_passing_empty_list,
        provider_create_data_with_regions,
        provider_create_data_with_idps,
    ),
    idstyle="explicit",
)


provider_create_invalid_data = fixture_union(
    "provider_create_invalid_data",
    (
        provider_create_invalid_pair,
        provider_create_duplicate_regions,
        provider_create_duplicate_projects,
        provider_create_duplicate_idps,
        provider_create_duplicate_sla_same_user_group,
        provider_create_invalid_sla_project_uuid,
        provider_create_invalid_block_storage_serv_project_uuid,
        provider_create_invalid_compute_serv_project_uuid,
        provider_create_invalid_network_serv_project_uuid,
    ),
    idstyle="explicit",
)
