from app.identity_provider.crud import identity_provider
from app.identity_provider.models import IdentityProvider
from app.identity_provider.schemas import IdentityProviderCreate, IdentityProviderUpdate
from app.tests.utils.utils import random_lower_string, random_url


def create_random_identity_provider() -> IdentityProvider:
    description = random_lower_string()
    endpoint = random_url()
    group_claim = random_lower_string()
    item_in = IdentityProviderCreate(
        description=description, endpoint=endpoint, group_claim=group_claim
    )
    return identity_provider.create(obj_in=item_in)


def create_random_update_identity_provider_data() -> IdentityProviderUpdate:
    description = random_lower_string()
    endpoint = random_url()
    group_claim = random_lower_string()
    return IdentityProviderUpdate(
        description=description, endpoint=endpoint, group_claim=group_claim
    )
