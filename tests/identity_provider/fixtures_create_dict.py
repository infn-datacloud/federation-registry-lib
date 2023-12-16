"""IdentityProvider specific fixtures."""
from typing import Any, Dict
from uuid import uuid4

from pytest_cases import fixture, fixture_union, parametrize

from app.provider.schemas_extended import (
    AuthMethodCreate,
    SLACreateExtended,
    UserGroupCreateExtended,
)
from tests.common.utils import (
    random_lower_string,
    random_start_end_dates,
    random_url,
)

invalid_create_key_values = [
    ("description", None),
    ("endpoint", None),
    ("group_claim", None),
]
relationships_num = [1, 2]


@fixture
def identity_provider_create_mandatory_data() -> Dict[str, Any]:
    """Dict with IdentityProvider mandatory attributes."""
    return {"endpoint": random_url(), "group_claim": random_lower_string()}


@fixture
def identity_provider_create_all_data(
    identity_provider_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all IdentityProvider attributes."""
    return {
        **identity_provider_create_mandatory_data,
        "description": random_lower_string(),
    }


@fixture
@parametrize(owned_user_groups=relationships_num)
def identity_provider_create_data_with_rel(
    owned_user_groups: int,
    identity_provider_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with IdentityProvider mandatory attributes."""
    start_date, end_date = random_start_end_dates()
    user_groups = []
    for _ in range(owned_user_groups):
        user_groups.append(
            UserGroupCreateExtended(
                name=random_lower_string(),
                sla=SLACreateExtended(
                    doc_uuid=uuid4(),
                    start_date=start_date,
                    end_date=end_date,
                    project=uuid4(),
                ),
            )
        )
    return {
        **identity_provider_create_mandatory_data,
        "relationship": AuthMethodCreate(
            idp_name=random_lower_string(), protocol=random_lower_string()
        ),
        "user_groups": user_groups,
    }


@fixture
@parametrize("k, v", invalid_create_key_values)
def identity_provider_create_invalid_pair(
    identity_provider_create_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    return {**identity_provider_create_mandatory_data, k: v}


@fixture
def identity_provider_create_invalid_user_group_list_size(
    identity_provider_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """User group list can't be empty."""
    return {**identity_provider_create_mandatory_data, "user_groups": []}


@fixture
def identity_provider_create_duplicate_user_groups(
    identity_provider_create_mandatory_data: Dict[str, Any],
    user_group_create_mandatory_data: Dict[str, Any],
):
    """Invalid case: the user group list has duplicate values."""
    start_date, end_date = random_start_end_dates()
    user_group = UserGroupCreateExtended(
        **user_group_create_mandatory_data,
        sla=SLACreateExtended(
            doc_uuid=uuid4(),
            start_date=start_date,
            end_date=end_date,
            project=uuid4(),
        ),
    )
    return {
        **identity_provider_create_mandatory_data,
        "user_groups": [user_group, user_group],
    }


identity_provider_create_valid_data = fixture_union(
    "identity_provider_create_valid_data",
    (identity_provider_create_data_with_rel,),
    idstyle="explicit",
)


identity_provider_create_invalid_data = fixture_union(
    "identity_provider_create_invalid_data",
    (
        identity_provider_create_mandatory_data,
        identity_provider_create_invalid_pair,
        identity_provider_create_invalid_user_group_list_size,
        identity_provider_create_duplicate_user_groups,
    ),
    idstyle="explicit",
)
