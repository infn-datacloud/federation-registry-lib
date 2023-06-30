from .utils import random_lower_string, random_url
from ...identity_provider.crud import identity_provider
from ...identity_provider.models import IdentityProvider
from ...identity_provider.schemas import IdentityProviderCreate


def create_random_identity_provider() -> IdentityProvider:
    description = random_lower_string()
    endpoint = random_url()
    item_in = IdentityProviderCreate(
        description=description, endpoint=endpoint
    )
    return identity_provider.create(obj_in=item_in)
