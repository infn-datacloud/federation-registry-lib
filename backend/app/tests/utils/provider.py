from app.provider.crud import provider
from app.provider.models import Provider
from app.provider.schemas import ProviderUpdate
from app.provider.schemas_extended import ProviderCreateExtended
from app.tests.utils.utils import random_bool, random_email, random_lower_string


def create_random_provider() -> Provider:
    description = random_lower_string()
    name = random_lower_string()
    is_public = random_bool()
    support_email = [random_email()]
    item_in = ProviderCreateExtended(
        description=description,
        name=name,
        is_public=is_public,
        support_email=support_email,
    )
    return provider.create(obj_in=item_in)


def create_random_update_provider_data() -> ProviderUpdate:
    description = random_lower_string()
    name = random_lower_string()
    is_public = random_bool()
    support_email = [random_email()]
    return ProviderUpdate(
        description=description,
        name=name,
        is_public=is_public,
        support_email=support_email,
    )
