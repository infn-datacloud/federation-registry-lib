import copy
from uuid import uuid4

import pytest
from app.provider.crud import provider
from app.provider.schemas import ProviderRead, ProviderReadPublic, ProviderReadShort
from app.provider.schemas_extended import (
    ProviderReadExtended,
    ProviderReadExtendedPublic,
)
from app.tests.utils.provider import create_random_provider
from app.tests.utils.utils import random_lower_string, random_url
from pydantic import ValidationError


def test_create_schema():
    """Create a valid 'Create' Schema."""
    create_random_provider()
    create_random_provider(default=True)
    create_random_provider(with_identity_providers=True)
    create_random_provider(default=True, with_identity_providers=True)
    create_random_provider(with_projects=True)
    create_random_provider(default=True, with_projects=True)
    create_random_provider(with_regions=True)
    create_random_provider(default=True, with_regions=True)
    create_random_provider(
        with_identity_providers=True, with_projects=True, with_regions=True
    )
    create_random_provider(
        default=True,
        with_identity_providers=True,
        with_projects=True,
        with_regions=True,
    )


def test_invalid_create_schema():
    """List all invalid situations for a 'Create' Schema."""
    a = create_random_provider(
        with_identity_providers=True, with_projects=True, with_regions=True
    )
    with pytest.raises(ValidationError):
        a.name = None
    with pytest.raises(ValidationError):
        a.type = None
    with pytest.raises(ValidationError):
        a.type = random_lower_string()
    with pytest.raises(ValidationError):
        a.status = None
    with pytest.raises(ValidationError):
        a.status = random_lower_string()
    with pytest.raises(ValidationError):
        # Duplicated identity providers
        a.identity_providers = [a.identity_providers[0], a.identity_providers[0]]
    with pytest.raises(ValidationError):
        # Duplicated identity projects
        a.projects = [a.projects[0], a.projects[0]]
    with pytest.raises(ValidationError):
        # Duplicated identity regions
        a.regions = [a.regions[0], a.regions[0]]
    with pytest.raises(ValidationError):
        # Different IDPs but duplicated SLAs.
        idp1 = a.identity_providers[0]
        idp2 = copy.deepcopy(idp1)
        idp2.endpoint = random_url()
        a.identity_providers = [idp1, idp2]
    with pytest.raises(ValidationError):
        # Project referenced by an SLA is not in the provider projects.
        idp = a.identity_providers[0]
        idp.user_groups[0].slas[0].projects = [uuid4()]
        a.identity_providers = [idp]
    with pytest.raises(ValidationError):
        # Project referenced by a Block Storage Quota is not in the provider projects.
        reg = a.regions[0]
        reg.block_storage_services[0].quotas[0].project = uuid4()
        a.regions = [reg]
    with pytest.raises(ValidationError):
        # Project referenced by a Flavor is not in the provider projects.
        reg = a.regions[0]
        reg.compute_services[0].flavors[0].projects = [uuid4()]
        a.regions = [reg]
    with pytest.raises(ValidationError):
        # Project referenced by an Image is not in the provider projects.
        reg = a.regions[0]
        reg.compute_services[0].images[0].projects = [uuid4()]
        a.regions = [reg]
    with pytest.raises(ValidationError):
        # Project referenced by a Compute Quota is not in the provider projects.
        reg = a.regions[0]
        reg.compute_services[0].quotas[0].project = uuid4()
        a.regions = [reg]
    with pytest.raises(ValidationError):
        # Project referenced by a Network is not in the provider projects.
        reg = a.regions[0]
        reg.network_services[0].networks[0].project = uuid4()
        a.regions = [reg]


def test_read_schema():
    """Create a valid 'Read' Schema."""
    obj_in = create_random_provider()
    db_obj = provider.create(obj_in=obj_in)
    ProviderRead.from_orm(db_obj)
    ProviderReadPublic.from_orm(db_obj)
    ProviderReadShort.from_orm(db_obj)
    ProviderReadExtended.from_orm(db_obj)
    ProviderReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_provider(default=True)
    db_obj = provider.create(obj_in=obj_in)
    ProviderRead.from_orm(db_obj)
    ProviderReadPublic.from_orm(db_obj)
    ProviderReadShort.from_orm(db_obj)
    ProviderReadExtended.from_orm(db_obj)
    ProviderReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_provider(with_projects=True)
    db_obj = provider.create(obj_in=obj_in)
    ProviderRead.from_orm(db_obj)
    ProviderReadPublic.from_orm(db_obj)
    ProviderReadShort.from_orm(db_obj)
    ProviderReadExtended.from_orm(db_obj)
    ProviderReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_provider(default=True, with_projects=True)
    db_obj = provider.create(obj_in=obj_in)
    ProviderRead.from_orm(db_obj)
    ProviderReadPublic.from_orm(db_obj)
    ProviderReadShort.from_orm(db_obj)
    ProviderReadExtended.from_orm(db_obj)
    ProviderReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_provider(with_identity_providers=True)
    db_obj = provider.create(obj_in=obj_in)
    ProviderRead.from_orm(db_obj)
    ProviderReadPublic.from_orm(db_obj)
    ProviderReadShort.from_orm(db_obj)
    ProviderReadExtended.from_orm(db_obj)
    ProviderReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_provider(default=True, with_identity_providers=True)
    db_obj = provider.create(obj_in=obj_in)
    ProviderRead.from_orm(db_obj)
    ProviderReadPublic.from_orm(db_obj)
    ProviderReadShort.from_orm(db_obj)
    ProviderReadExtended.from_orm(db_obj)
    ProviderReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_provider(with_regions=True)
    db_obj = provider.create(obj_in=obj_in)
    ProviderRead.from_orm(db_obj)
    ProviderReadPublic.from_orm(db_obj)
    ProviderReadShort.from_orm(db_obj)
    ProviderReadExtended.from_orm(db_obj)
    ProviderReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_provider(default=True, with_regions=True)
    db_obj = provider.create(obj_in=obj_in)
    ProviderRead.from_orm(db_obj)
    ProviderReadPublic.from_orm(db_obj)
    ProviderReadShort.from_orm(db_obj)
    ProviderReadExtended.from_orm(db_obj)
    ProviderReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_provider(
        with_projects=True, with_identity_providers=True, with_regions=True
    )
    db_obj = provider.create(obj_in=obj_in)
    ProviderRead.from_orm(db_obj)
    ProviderReadPublic.from_orm(db_obj)
    ProviderReadShort.from_orm(db_obj)
    ProviderReadExtended.from_orm(db_obj)
    ProviderReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_provider(
        default=True,
        with_projects=True,
        with_identity_providers=True,
        with_regions=True,
    )
    db_obj = provider.create(obj_in=obj_in)
    ProviderRead.from_orm(db_obj)
    ProviderReadPublic.from_orm(db_obj)
    ProviderReadShort.from_orm(db_obj)
    ProviderReadExtended.from_orm(db_obj)
    ProviderReadExtendedPublic.from_orm(db_obj)
