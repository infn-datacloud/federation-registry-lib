"""Provider specific fixtures."""
from typing import Any, Dict, Optional, Tuple

from pytest_cases import fixture, parametrize

from app.identity_provider.crud import identity_provider_mng
from app.project.crud import project_mng
from app.provider.crud import CRUDProvider, provider_mng
from app.provider.enum import ProviderStatus, ProviderType
from app.provider.models import Provider
from app.provider.schemas import ProviderBase, ProviderBasePublic, ProviderUpdate
from app.provider.schemas_extended import ProviderCreateExtended
from app.region.crud import region_mng
from tests.common.crud.validators import (
    CreateOperationValidation,
    DeleteOperationValidation,
    PatchOperationValidation,
    ReadOperationValidation,
)
from tests.common.utils import random_bool
from tests.provider.utils import random_status, random_type


@fixture
@parametrize(attr=[*ProviderBase.__fields__.keys()])
def provider_attr(attr: str) -> Optional[str]:
    """Parametrized provider attribute."""
    return attr


@fixture
def provider_not_existing_actors() -> CRUDProvider:
    """Return provider manager."""
    return provider_mng


@fixture
def provider_create_item_actors(
    provider_create_valid_data: Dict[str, Any],
) -> Tuple[
    CRUDProvider,
    CreateOperationValidation[
        ProviderBase, ProviderBasePublic, ProviderCreateExtended, Provider
    ],
    ProviderCreateExtended,
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    validator = CreateOperationValidation[
        ProviderBase, ProviderBasePublic, ProviderCreateExtended, Provider
    ](base=ProviderBase, base_public=ProviderBasePublic, create=ProviderCreateExtended)
    return (
        provider_mng,
        validator,
        ProviderCreateExtended(**provider_create_valid_data),
        {},
    )


@fixture
def provider_read_item_actors(
    db_provider_simple: Provider,
) -> Tuple[
    CRUDProvider,
    ReadOperationValidation[ProviderBase, ProviderBasePublic, Provider],
    Provider,
]:
    """Fixture with the read class, validator and the db item to read."""
    validator = ReadOperationValidation[ProviderBase, ProviderBasePublic, Provider](
        base=ProviderBase, base_public=ProviderBasePublic
    )
    return provider_mng, validator, db_provider_simple


@fixture
def provider_read_items_actors(
    db_provider_simple: Provider, db_provider_with_single_project: Provider
) -> Tuple[
    CRUDProvider,
    ReadOperationValidation[ProviderBase, ProviderBasePublic, Provider],
    Provider,
]:
    """Fixture with the read class, validator and the db items to read."""
    validator = ReadOperationValidation[ProviderBase, ProviderBasePublic, Provider](
        base=ProviderBase, base_public=ProviderBasePublic
    )
    return (
        provider_mng,
        validator,
        [db_provider_simple, db_provider_with_single_project],
    )


@fixture
def provider_delete_item_actors(
    db_provider: Provider,
) -> Tuple[
    CRUDProvider,
    DeleteOperationValidation[ProviderBase, ProviderBasePublic, Provider],
    Provider,
]:
    """Fixture with the delete class, validator and the db items to read."""
    validator = DeleteOperationValidation[ProviderBase, ProviderBasePublic, Provider](
        base=ProviderBase,
        base_public=ProviderBasePublic,
        managers={
            "identity_providers": identity_provider_mng,
            "projects": project_mng,
            "regions": region_mng,
        },
    )
    return provider_mng, validator, db_provider


@fixture
def provider_patch_item_actors(
    db_provider_simple: Provider, provider_patch_valid_data: Dict[str, Any]
) -> Tuple[
    CRUDProvider,
    PatchOperationValidation[ProviderBase, ProviderBasePublic, Provider],
    Provider,
    ProviderUpdate,
]:
    """Fixture with the delete class, validator and the db items to read."""
    validator = PatchOperationValidation[ProviderBase, ProviderBasePublic, Provider](
        base=ProviderBase, base_public=ProviderBasePublic
    )
    for k in provider_patch_valid_data.keys():
        while db_provider_simple.__getattribute__(k) == provider_patch_valid_data[k]:
            schema_type = ProviderUpdate.__fields__.get(k).type_
            if schema_type == bool:
                provider_patch_valid_data[k] = random_bool()
            elif schema_type == ProviderStatus:
                provider_patch_valid_data[k] = random_status()
            elif schema_type == ProviderType:
                provider_patch_valid_data[k] = random_type()
            else:
                print(schema_type)
                assert 0
    return (
        provider_mng,
        validator,
        db_provider_simple,
        ProviderUpdate(**provider_patch_valid_data),
    )


@fixture
def provider_patch_item_no_changes_actors(
    db_provider_simple: Provider, provider_attr: str
) -> Tuple[CRUDProvider, Provider, ProviderUpdate]:
    """Fixture with the delete class, validator and the db items to read."""
    provider_patch_valid_data = {
        provider_attr: db_provider_simple.__getattribute__(provider_attr)
    }
    return (
        provider_mng,
        db_provider_simple,
        ProviderUpdate(**provider_patch_valid_data),
    )


# @fixture
# def provider_create_invalid_schema_actors(
#     provider_create_invalid_data,
# ) -> Tuple[Type[ProviderCreateExtended], Dict[str, Any]]:
#     """Fixture with the create class and the invalid data to validate."""
#     return ProviderCreateExtended, provider_create_invalid_data


# @fixture
# def provider_patch_valid_schema_actors(
#     provider_patch_validator, provider_patch_valid_data
# ) -> Tuple[
#     Type[ProviderUpdate],
#     PatchSchemaValidation[ProviderBase, ProviderBasePublic],
#     Dict[str, Any],
# ]:
#     """Fixture with the update class, validator and data to validate."""
#     return ProviderUpdate, provider_patch_validator, provider_patch_valid_data


# @fixture
# def provider_patch_invalid_schema_actors(
#     provider_patch_invalid_data,
# ) -> Tuple[Type[ProviderUpdate], Dict[str, Any]]:
#     """Fixture with the update class and the invalid data to validate."""
#     return ProviderUpdate, provider_patch_invalid_data
