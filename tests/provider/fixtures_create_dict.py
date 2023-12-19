"""Provider specific fixtures."""
from typing import Any, Dict
from uuid import uuid4

from pytest_cases import fixture, fixture_union, parametrize

from tests.common.utils import random_lower_string
from tests.flavor.utils import random_flavor_required_attr, random_flavor_required_rel
from tests.identity_provider.utils import (
    random_identity_provider_required_attr,
    random_identity_provider_required_rel,
)
from tests.image.utils import random_image_required_attr, random_image_required_rel
from tests.network.utils import (
    random_network_required_attr,
    random_network_required_rel,
)
from tests.project.utils import random_project_required_attr
from tests.provider.utils import (
    random_provider_all_attr,
    random_provider_required_attr,
    random_provider_required_rel,
)
from tests.quotas.block_storage_quota.utils import (
    random_block_storage_quota_required_attr,
    random_block_storage_quota_required_rel,
)
from tests.quotas.compute_quota.utils import (
    random_compute_quota_required_attr,
    random_compute_quota_required_rel,
)
from tests.quotas.network_quota.utils import (
    random_network_quota_required_attr,
    random_network_quota_required_rel,
)
from tests.region.utils import random_region_required_attr
from tests.services.block_storage_service.utils import (
    random_block_storage_service_required_attr,
)
from tests.services.compute_service.utils import random_compute_service_required_attr
from tests.services.network_service.utils import random_network_service_required_attr
from tests.sla.utils import random_sla_required_attr
from tests.user_group.utils import random_user_group_required_attr

invalid_create_key_values = [
    ("description", None),
    ("name", None),
    ("type", None),
    ("type", random_lower_string()),
    ("status", None),
    ("status", random_lower_string()),
    ("is_public", None),
]


@fixture
def provider_create_minimum_data() -> Dict[str, Any]:
    """Dict with Provider mandatory attributes."""
    return random_provider_required_attr()


@fixture
@parametrize(attr=["identity_providers", "projects", "regions"])
def provider_create_data_passing_empty_list(attr: str) -> Dict[str, Any]:
    """Dict with all Provider attributes.

    Passing an empty list is not a problem.
    """
    return {**random_provider_all_attr(), attr: []}


@fixture
def provider_create_data_with_regions() -> Dict[str, Any]:
    """Dict with all Provider attributes and regions."""
    return {**random_provider_all_attr(), "regions": [random_region_required_attr()]}


@fixture
def provider_create_data_with_projects() -> Dict[str, Any]:
    """Dict with all Provider attributes and regions."""
    return {**random_provider_all_attr(), "projects": [random_project_required_attr()]}


@fixture
def provider_create_data_with_idps() -> Dict[str, Any]:
    """Dict with all Provider attributes and regions."""
    project = random_project_required_attr()
    return {
        **random_provider_all_attr(),
        "projects": [project],
        "identity_providers": [
            {
                **random_identity_provider_required_attr(),
                **random_identity_provider_required_rel(),
                "user_groups": [
                    {
                        **random_user_group_required_attr(),
                        "sla": {
                            **random_sla_required_attr(),
                            "project": project["uuid"],
                        },
                    }
                ],
            }
        ],
    }


@fixture
@parametrize("k, v", invalid_create_key_values)
def provider_create_invalid_pair(k: str, v: Any) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    return {**random_provider_required_attr(), k: v}


@fixture
def provider_create_duplicate_regions() -> Dict[str, Any]:
    """Dict with all Provider attributes and regions."""
    region = random_region_required_attr()
    return {**random_provider_required_attr(), "regions": [region, region]}


@fixture
def provider_create_duplicate_projects() -> Dict[str, Any]:
    """Dict with all Provider attributes and regions."""
    project = random_project_required_attr()
    return {**random_provider_required_attr(), "projects": [project, project]}


@fixture
def provider_create_duplicate_idps() -> Dict[str, Any]:
    """Dict with all Provider attributes and regions."""
    projects = [random_project_required_attr(), random_project_required_attr()]
    idp_data = random_identity_provider_required_attr()
    identity_providers = []
    for project in projects:
        identity_providers.append(
            {
                **idp_data,
                **random_identity_provider_required_rel(),
                "user_groups": [
                    {
                        **random_user_group_required_attr(),
                        "sla": {
                            **random_sla_required_attr(),
                            "project": project["uuid"],
                        },
                    }
                ],
            }
        )
    return {
        **random_provider_required_attr(),
        "projects": projects,
        "identity_providers": identity_providers,
    }


@fixture
def provider_create_duplicate_sla_same_user_group() -> Dict[str, Any]:
    """Dict with all Provider attributes and regions."""
    projects = [random_project_required_attr(), random_project_required_attr()]
    identity_providers = []
    sla_uuid = uuid4()
    for project in projects:
        identity_providers.append(
            {
                **random_identity_provider_required_attr(),
                **random_identity_provider_required_rel(),
                "user_groups": [
                    {
                        **random_user_group_required_attr(),
                        "sla": {
                            **random_sla_required_attr(),
                            "doc_uuid": sla_uuid,
                            "project": project["uuid"],
                        },
                    }
                ],
            }
        )
    return {
        **random_provider_required_attr(),
        "projects": projects,
        "identity_providers": identity_providers,
    }


@fixture
def provider_create_invalid_sla_project_uuid() -> Dict[str, Any]:
    """Dict with all Provider attributes and regions."""
    return {**random_provider_required_attr(), **random_provider_required_rel()}


@fixture
def provider_create_invalid_block_storage_serv_project_uuid() -> Dict[str, Any]:
    """Dict with all Provider attributes and regions."""
    return {
        **random_project_required_attr(),
        "regions": [
            {
                **random_region_required_attr(),
                "block_storage_services": [
                    {
                        **random_block_storage_service_required_attr(),
                        "quotas": [
                            {
                                **random_block_storage_quota_required_attr(),
                                **random_block_storage_quota_required_rel(),
                            }
                        ],
                    }
                ],
            },
        ],
    }


@fixture
@parametrize(service_rel_type=["flavors, images, quotas"])
def provider_create_invalid_compute_serv_project_uuid(
    service_rel_type: str,
) -> Dict[str, Any]:
    """Dict with all Provider attributes and regions."""
    compute_service = random_compute_service_required_attr()
    if service_rel_type == "flavors":
        compute_service[service_rel_type] = {
            **random_flavor_required_attr(),
            **random_flavor_required_rel(False),
            "is_public": False,
        }
    if service_rel_type == "images":
        compute_service[service_rel_type] = {
            **random_image_required_attr(),
            **random_image_required_rel(False),
            "is_public": False,
        }
    if service_rel_type == "quotas":
        compute_service[service_rel_type] = {
            **random_compute_quota_required_attr(),
            **random_compute_quota_required_rel(),
        }
    return {
        **random_project_required_attr(),
        "regions": [
            {**random_region_required_attr(), "compute_services": [compute_service]}
        ],
    }


@fixture
@parametrize(service_rel_type=["networks, quotas"])
def provider_create_invalid_network_serv_project_uuid(
    service_rel_type: str,
) -> Dict[str, Any]:
    """Dict with all Provider attributes and regions."""
    network_service = random_network_service_required_attr()
    if service_rel_type == "networks":
        network_service[service_rel_type] = {
            **random_network_required_attr(),
            **random_network_required_rel(False),
            "is_shared": False,
        }
    if service_rel_type == "quotas":
        network_service[service_rel_type] = {
            **random_network_quota_required_attr(),
            **random_network_quota_required_rel(),
        }
    return {
        **random_project_required_attr(),
        "regions": [
            {**random_region_required_attr(), "network_services": [network_service]}
        ],
    }


provider_create_valid_data = fixture_union(
    "provider_create_valid_data",
    (
        provider_create_minimum_data,
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

provider_create_with_rel = fixture_union(
    "provider_create_with_rel",
    [
        provider_create_data_with_idps,
        provider_create_data_with_projects,
        provider_create_data_with_regions,
    ],
    idstyle="explicit",
)
