from .utils import random_bool, random_email, random_lower_string
from ...provider.crud import provider
from ...provider.models import Provider
from ...provider.schemas import ProviderCreate


def create_random_provider() -> Provider:
    description = random_lower_string()
    name = random_lower_string()
    is_public = random_bool()
    support_email = [random_email()]
    item_in = ProviderCreate(
        description=description,
        name=name,
        is_public=is_public,
        support_email=support_email,
    )
    return provider.create(obj_in=item_in)
