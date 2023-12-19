"""Provider specific fixtures."""
import copy
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
from tests.identity_provider.utils import (
    random_identity_provider_required_attr,
    random_identity_provider_required_rel,
)
from tests.project.utils import random_project_required_attr
from tests.provider.utils import (
    random_provider_required_attr,
    random_status,
    random_type,
)
from tests.region.utils import random_region_required_attr


@fixture
@parametrize(attr=[*ProviderBase.__fields__.keys()])
def provider_attr(attr: str) -> Optional[str]:
    """Parametrized provider attribute."""
    return attr


@fixture
@parametrize(attr=[k for k, v in ProviderBase.__fields__.items() if not v.required])
def provider_valid_patch_default_attr(attr: str) -> Optional[str]:
    """Parametrized provider attribute."""
    return attr


@fixture
@parametrize(attr=[k for k, v in ProviderBase.__fields__.items() if v.required])
def provider_invalid_patch_default_attr(attr: str) -> Optional[str]:
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
def provider_patch_item_with_default_actors(
    db_provider_no_defaults: Provider, provider_valid_patch_default_attr: str
) -> Tuple[CRUDProvider, Provider, ProviderUpdate]:
    """Fixture with the delete class, validator and the db items to read."""
    validator = PatchOperationValidation[ProviderBase, ProviderBasePublic, Provider](
        base=ProviderBase, base_public=ProviderBasePublic
    )
    field_data = ProviderUpdate.__fields__.get(provider_valid_patch_default_attr)
    provider_patch_valid_data = {
        provider_valid_patch_default_attr: field_data.get_default()
    }
    return (
        provider_mng,
        validator,
        db_provider_no_defaults,
        ProviderUpdate(**provider_patch_valid_data),
    )


@fixture
def provider_patch_item_required_with_none_actors(
    db_provider_no_defaults: Provider, provider_invalid_patch_default_attr: str
) -> Tuple[CRUDProvider, Provider, ProviderUpdate]:
    """Fixture with the delete class, validator and the db items to read."""
    field_data = ProviderUpdate.__fields__.get(provider_invalid_patch_default_attr)
    provider_patch_valid_data = {
        provider_invalid_patch_default_attr: field_data.get_default()
    }
    return (
        provider_mng,
        db_provider_no_defaults,
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


@fixture
def provider_force_update_unchanged_rel_actors(
    provider_create_with_rel: Dict[str, Any],
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
    db_item = provider_mng.create(
        obj_in=ProviderCreateExtended(**provider_create_with_rel)
    )
    for k, v in random_provider_required_attr().items():
        provider_create_with_rel[k] = v
    return (
        provider_mng,
        validator,
        db_item,
        ProviderCreateExtended(**provider_create_with_rel),
    )


@fixture
@parametrize(start_empty=[True, False])
def provider_force_update_add_rel_actors(
    start_empty: bool, provider_create_with_rel: Dict[str, Any]
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
    if start_empty:
        starting_data = {
            **copy.deepcopy(provider_create_with_rel),
            "identity_providers": [],
            "projects": [],
            "regions": [],
        }
        new_data = copy.deepcopy(provider_create_with_rel)
    else:
        starting_data = copy.deepcopy(provider_create_with_rel)
        new_data = copy.deepcopy(provider_create_with_rel)
        if len(new_data.get("regions", [])) > 0:
            new_data["regions"].append(random_region_required_attr())
        if len(new_data.get("projects", [])) > 0:
            new_data["projects"].append(random_project_required_attr())
        if len(new_data.get("identity_providers", [])) > 0:
            new_data["identity_providers"].append(
                {
                    **random_identity_provider_required_attr(),
                    **random_identity_provider_required_rel(),
                }
            )
            new_data["identity_providers"][-1]["user_groups"][0]["sla"][
                "project"
            ] = new_data["projects"][-1]["uuid"]
    db_item = provider_mng.create(obj_in=ProviderCreateExtended(**starting_data))
    return provider_mng, validator, db_item, ProviderCreateExtended(**new_data)


@fixture
@parametrize(end_empty=[True, False])
def provider_force_update_remove_rel_actors(
    end_empty: bool, provider_create_with_rel: Dict[str, Any]
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
    if end_empty:
        starting_data = copy.deepcopy(provider_create_with_rel)
        new_data = {
            **copy.deepcopy(provider_create_with_rel),
            "identity_providers": [],
            "projects": [],
            "regions": [],
        }
    else:
        starting_data = copy.deepcopy(provider_create_with_rel)
        if len(starting_data.get("regions", [])) > 0:
            starting_data["regions"].append(random_region_required_attr())
        if len(starting_data.get("projects", [])) > 0:
            starting_data["projects"].append(random_project_required_attr())
        if len(starting_data.get("identity_providers", [])) > 0:
            starting_data["identity_providers"].append(
                {
                    **random_identity_provider_required_attr(),
                    **random_identity_provider_required_rel(),
                }
            )
            starting_data["identity_providers"][-1]["user_groups"][0]["sla"][
                "project"
            ] = starting_data["projects"][-1]["uuid"]
        new_data = copy.deepcopy(provider_create_with_rel)
    db_item = provider_mng.create(obj_in=ProviderCreateExtended(**starting_data))
    return provider_mng, validator, db_item, ProviderCreateExtended(**new_data)


@fixture
@parametrize(replace_all=[True, False])
def provider_force_update_replace_rel_actors(
    replace_all: bool, provider_create_with_rel: Dict[str, Any]
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
    if replace_all:
        starting_data = copy.deepcopy(provider_create_with_rel)
    else:
        starting_data = copy.deepcopy(provider_create_with_rel)
        if len(starting_data.get("regions", [])) > 0:
            starting_data["regions"].append(random_region_required_attr())
        if len(starting_data.get("projects", [])) > 0:
            starting_data["projects"].append(random_project_required_attr())
        if len(starting_data.get("identity_providers", [])) > 0:
            starting_data["identity_providers"].append(
                {
                    **random_identity_provider_required_attr(),
                    **random_identity_provider_required_rel(),
                }
            )
            starting_data["identity_providers"][-1]["user_groups"][0]["sla"][
                "project"
            ] = starting_data["projects"][-1]["uuid"]
    new_data = copy.deepcopy(provider_create_with_rel)
    if len(new_data.get("regions", [])) > 0:
        new_data["regions"] = [random_region_required_attr()]
    if len(new_data.get("projects", [])) > 0:
        new_data["projects"] = [random_project_required_attr()]
    if len(new_data.get("identity_providers", [])) > 0:
        new_data["identity_providers"] = [
            {
                **new_data["identity_providers"][0],
                **random_identity_provider_required_attr(),
            }
        ]
        new_data["identity_providers"][-1]["user_groups"][0]["sla"][
            "project"
        ] = new_data["projects"][-1]["uuid"]
    db_item = provider_mng.create(obj_in=ProviderCreateExtended(**starting_data))
    return provider_mng, validator, db_item, ProviderCreateExtended(**new_data)
