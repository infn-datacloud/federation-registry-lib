"""IdentityProvider specific fixtures."""
from typing import Any, Dict
from uuid import uuid4

from pytest_cases import fixture, fixture_union, parametrize

from app.provider.schemas_extended import (
    AuthMethodCreate,
    SLACreateExtended,
    UserGroupCreateExtended,
)
from tests.common.utils import random_lower_string
from tests.identity_provider.utils import (
    random_identity_provider_all_attr,
    random_identity_provider_required_attr,
)
from tests.sla.utils import random_sla_required_attr
from tests.user_group.utils import random_user_group_required_attr

invalid_create_key_values = [
    ("description", None),
    ("endpoint", None),
    ("group_claim", None),
]


@fixture
def identity_provider_create_minimum_data() -> Dict[str, Any]:
    """Dict with IdentityProvider mandatory attributes."""
    return random_identity_provider_required_attr()


@fixture
@parametrize(owned_user_groups=[1, 2])  # TODO evaluate if to use onnly one user group
def identity_provider_create_data_with_rel(owned_user_groups: int) -> Dict[str, Any]:
    """Dict with IdentityProvider mandatory attributes."""
    user_groups = []
    for _ in range(owned_user_groups):
        user_groups.append(
            UserGroupCreateExtended(
                **random_user_group_required_attr(),
                sla=SLACreateExtended(**random_sla_required_attr(), project=uuid4()),
            )
        )
    return {
        **random_identity_provider_all_attr(),
        "relationship": AuthMethodCreate(
            idp_name=random_lower_string(), protocol=random_lower_string()
        ),
        "user_groups": user_groups,
    }


@fixture
@parametrize("k, v", invalid_create_key_values)
def identity_provider_create_invalid_pair(
    identity_provider_create_data_with_rel: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    return {**identity_provider_create_data_with_rel, k: v}


@fixture
def identity_provider_create_invalid_user_group_list_size(
    identity_provider_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """User group list can't be empty."""
    return {**identity_provider_create_data_with_rel, "user_groups": []}


@fixture
def identity_provider_create_duplicate_user_groups(
    identity_provider_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Invalid case: the user group list has duplicate values."""
    user_group_data = random_user_group_required_attr()
    user_groups = [
        UserGroupCreateExtended(
            **user_group_data,
            sla=SLACreateExtended(**random_sla_required_attr(), project=uuid4()),
        ),
        UserGroupCreateExtended(
            **user_group_data,
            sla=SLACreateExtended(**random_sla_required_attr(), project=uuid4()),
        ),
    ]
    return {**identity_provider_create_data_with_rel, "user_groups": user_groups}


identity_provider_create_valid_data = fixture_union(
    "identity_provider_create_valid_data",
    (identity_provider_create_data_with_rel,),
    idstyle="explicit",
)


identity_provider_create_invalid_data = fixture_union(
    "identity_provider_create_invalid_data",
    (
        identity_provider_create_minimum_data,
        identity_provider_create_invalid_pair,
        identity_provider_create_invalid_user_group_list_size,
        identity_provider_create_duplicate_user_groups,
    ),
    idstyle="explicit",
)
