from typing import List

from app.auth_method.schemas import AuthMethodCreate
from app.identity_provider.models import IdentityProvider
from app.identity_provider.schemas import IdentityProviderUpdate
from app.provider.schemas_extended import IdentityProviderCreateExtended
from app.tests.utils.user_group import (
    create_random_user_group,
    validate_user_group_attrs,
)
from app.tests.utils.utils import random_lower_string, random_url
from pydantic import UUID4


def create_random_identity_provider(
    *, default: bool = False, projects: List[UUID4] = []
) -> IdentityProviderCreateExtended:
    endpoint = random_url()
    group_claim = random_lower_string()
    relationship = random_relationship()
    user_groups = [create_random_user_group(projects=projects)]
    kwargs = {}
    if not default:
        kwargs = {"description": random_lower_string()}
    return IdentityProviderCreateExtended(
        endpoint=endpoint,
        group_claim=group_claim,
        relationship=relationship,
        user_groups=user_groups,
        **kwargs
    )


def create_random_update_identity_provider_data() -> IdentityProviderUpdate:
    description = random_lower_string()
    endpoint = random_url()
    group_claim = random_lower_string()
    return IdentityProviderUpdate(
        description=description, endpoint=endpoint, group_claim=group_claim
    )


def random_relationship() -> AuthMethodCreate:
    idp_name = random_lower_string()
    protocol = random_lower_string()
    return AuthMethodCreate(idp_name=idp_name, protocol=protocol)


def validate_identity_provider_attrs(
    *, obj_in: IdentityProviderCreateExtended, db_item: IdentityProvider
) -> None:
    assert db_item.description == obj_in.description
    assert db_item.endpoint == obj_in.endpoint
    assert db_item.group_claim == obj_in.group_claim
    # TODO validate relationship
    assert len(db_item.user_groups) == len(obj_in.user_groups)
    for db_user, user_in in zip(db_item.user_groups, obj_in.user_groups):
        validate_user_group_attrs(obj_in=user_in, db_item=db_user)
