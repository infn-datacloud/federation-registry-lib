import copy
from uuid import uuid4

import pytest
from app.provider.models import Provider
from app.provider.schemas import ProviderRead, ProviderReadPublic, ProviderReadShort
from app.provider.schemas_extended import (
    ProviderReadExtended,
    ProviderReadExtendedPublic,
)
from pydantic import ValidationError
from tests.utils.provider import (
    create_random_provider,
    validate_read_extended_provider_attrs,
    validate_read_extended_public_provider_attrs,
    validate_read_provider_attrs,
    validate_read_public_provider_attrs,
    validate_read_short_provider_attrs,
)
from tests.utils.utils import random_lower_string, random_url


def test_create_schema():
    """Create a valid 'Create' Schema."""
    create_random_provider()
    create_random_provider(default=True)
    create_random_provider(with_projects=True)
    create_random_provider(default=True, with_projects=True)
    create_random_provider(with_projects=True, with_identity_providers=True)
    create_random_provider(
        default=True, with_projects=True, with_identity_providers=True
    )
    create_random_provider(with_regions=True)
    create_random_provider(default=True, with_regions=True)
    create_random_provider(
        with_projects=True, with_identity_providers=True, with_regions=True
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
        idp.user_groups[0].sla.project = uuid4()
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


def test_read_schema_no_relationships(db_provider: Provider):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target provider has no relationships.
    """
    schema = ProviderRead.from_orm(db_provider)
    validate_read_provider_attrs(obj_out=schema, db_item=db_provider)
    schema = ProviderReadShort.from_orm(db_provider)
    validate_read_short_provider_attrs(obj_out=schema, db_item=db_provider)
    schema = ProviderReadPublic.from_orm(db_provider)
    validate_read_public_provider_attrs(obj_out=schema, db_item=db_provider)
    schema = ProviderReadExtended.from_orm(db_provider)
    validate_read_extended_provider_attrs(obj_out=schema, db_item=db_provider)
    schema = ProviderReadExtendedPublic.from_orm(db_provider)
    validate_read_extended_public_provider_attrs(obj_out=schema, db_item=db_provider)


def test_read_schema_with_single_idp(db_provider_with_single_idp: Provider):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target provider has one idp and one project.
    """
    schema = ProviderRead.from_orm(db_provider_with_single_idp)
    validate_read_provider_attrs(obj_out=schema, db_item=db_provider_with_single_idp)
    schema = ProviderReadShort.from_orm(db_provider_with_single_idp)
    validate_read_short_provider_attrs(
        obj_out=schema, db_item=db_provider_with_single_idp
    )
    schema = ProviderReadPublic.from_orm(db_provider_with_single_idp)
    validate_read_public_provider_attrs(
        obj_out=schema, db_item=db_provider_with_single_idp
    )
    schema = ProviderReadExtended.from_orm(db_provider_with_single_idp)
    validate_read_extended_provider_attrs(
        obj_out=schema, db_item=db_provider_with_single_idp
    )
    schema = ProviderReadExtendedPublic.from_orm(db_provider_with_single_idp)
    validate_read_extended_public_provider_attrs(
        obj_out=schema, db_item=db_provider_with_single_idp
    )


def test_read_schema_with_multiple_idps(
    db_provider_with_multiple_idps: Provider,
):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target provider support multiple idps and has multiple project.
    """
    schema = ProviderRead.from_orm(db_provider_with_multiple_idps)
    validate_read_provider_attrs(obj_out=schema, db_item=db_provider_with_multiple_idps)
    schema = ProviderReadShort.from_orm(db_provider_with_multiple_idps)
    validate_read_short_provider_attrs(
        obj_out=schema, db_item=db_provider_with_multiple_idps
    )
    schema = ProviderReadPublic.from_orm(db_provider_with_multiple_idps)
    validate_read_public_provider_attrs(
        obj_out=schema, db_item=db_provider_with_multiple_idps
    )
    schema = ProviderReadExtended.from_orm(db_provider_with_multiple_idps)
    validate_read_extended_provider_attrs(
        obj_out=schema, db_item=db_provider_with_multiple_idps
    )
    schema = ProviderReadExtendedPublic.from_orm(db_provider_with_multiple_idps)
    validate_read_extended_public_provider_attrs(
        obj_out=schema, db_item=db_provider_with_multiple_idps
    )


def test_read_schema_with_single_region(db_provider_with_single_region: Provider):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target provider has one region.
    """
    schema = ProviderRead.from_orm(db_provider_with_single_region)
    validate_read_provider_attrs(obj_out=schema, db_item=db_provider_with_single_region)
    schema = ProviderReadShort.from_orm(db_provider_with_single_region)
    validate_read_short_provider_attrs(
        obj_out=schema, db_item=db_provider_with_single_region
    )
    schema = ProviderReadPublic.from_orm(db_provider_with_single_region)
    validate_read_public_provider_attrs(
        obj_out=schema, db_item=db_provider_with_single_region
    )
    schema = ProviderReadExtended.from_orm(db_provider_with_single_region)
    validate_read_extended_provider_attrs(
        obj_out=schema, db_item=db_provider_with_single_region
    )
    schema = ProviderReadExtendedPublic.from_orm(db_provider_with_single_region)
    validate_read_extended_public_provider_attrs(
        obj_out=schema, db_item=db_provider_with_single_region
    )


def test_read_schema_with_multiple_regions(
    db_provider_with_multiple_regions: Provider,
):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target provider has multiple regions.
    """
    schema = ProviderRead.from_orm(db_provider_with_multiple_regions)
    validate_read_provider_attrs(
        obj_out=schema, db_item=db_provider_with_multiple_regions
    )
    schema = ProviderReadShort.from_orm(db_provider_with_multiple_regions)
    validate_read_short_provider_attrs(
        obj_out=schema, db_item=db_provider_with_multiple_regions
    )
    schema = ProviderReadPublic.from_orm(db_provider_with_multiple_regions)
    validate_read_public_provider_attrs(
        obj_out=schema, db_item=db_provider_with_multiple_regions
    )
    schema = ProviderReadExtended.from_orm(db_provider_with_multiple_regions)
    validate_read_extended_provider_attrs(
        obj_out=schema, db_item=db_provider_with_multiple_regions
    )
    schema = ProviderReadExtendedPublic.from_orm(db_provider_with_multiple_regions)
    validate_read_extended_public_provider_attrs(
        obj_out=schema, db_item=db_provider_with_multiple_regions
    )


# TODO
# def test_read_schema_with_everything(db_provider_with_everything: Provider):
#     """Create a valid 'Read' Schema from DB object.

#     Apply conversion for this item for all read
#     schemas. No one of them should raise errors.

#     Target provider has projects, authorized idps and regions."""
#     schema = ProviderRead.from_orm(db_provider_with_everything)
#     validate_read_provider_attrs(obj_out=schema, db_item=db_provider_with_everything)
#     schema = ProviderReadShort.from_orm(db_provider_with_everything)
#     validate_read_short_provider_attrs(
#         obj_out=schema, db_item=db_provider_with_everything
#     )
#     schema = ProviderReadPublic.from_orm(db_provider_with_everything)
#     validate_read_public_provider_attrs(
#         obj_out=schema, db_item=db_provider_with_everything
#     )
#     schema = ProviderReadExtended.from_orm(db_provider_with_everything)
#     validate_read_extended_provider_attrs(
#         obj_out=schema, db_item=db_provider_with_everything
#     )
#     schema = ProviderReadExtendedPublic.from_orm(db_provider_with_everything)
#     validate_read_extended_public_provider_attrs(
#         obj_out=schema, db_item=db_provider_with_everything
#     )
