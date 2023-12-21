"""Provider specific fixtures."""
import copy
from typing import Any, Dict, List, Optional, Tuple

from pytest_cases import case, parametrize

from app.identity_provider.crud import identity_provider_mng
from app.project.crud import project_mng
from app.provider.crud import CRUDProvider, provider_mng
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
from tests.identity_provider.utils import random_identity_provider_required_attr
from tests.project.utils import random_project_required_attr
from tests.provider.fixtures_patch_dict import (
    provider_force_update_enriched_relationships_data,
    provider_patch_not_equal_data,
)
from tests.provider.utils import random_provider_required_attr
from tests.region.utils import random_region_required_attr

provider_get_attr = [*ProviderBase.__fields__.keys(), "uid", None]
provider_sort_attr = [*ProviderBase.__fields__.keys(), "uid"]
provider_patch_attr = [*ProviderBase.__fields__.keys()]
provider_patch_default_attr = [
    k for k, v in ProviderBase.__fields__.items() if not v.required
]
provider_patch_required_attr = [
    k for k, v in ProviderBase.__fields__.items() if v.required
]


@case(tags=["provider", "not_existing"])
def case_provider_not_existing_actors() -> CRUDProvider:
    """Return provider manager."""
    return provider_mng


@case(tags=["provider", "create_item"])
def case_provider_create_item_actors(
    provider_create_valid_data: Dict[str, Any],
) -> Tuple[
    CRUDProvider,
    CreateOperationValidation[
        ProviderBase, ProviderBasePublic, ProviderCreateExtended, Provider
    ],
    ProviderCreateExtended,
    Dict[str, Any],
    List[str],
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
        [],
    )


@case(tags=["provider", "read_single"])
@parametrize(attr=provider_get_attr)
def case_provider_read_item_actors(
    db_provider_no_defaults: Provider, attr: str
) -> Tuple[
    CRUDProvider,
    ReadOperationValidation[ProviderBase, ProviderBasePublic, Provider],
    Provider,
    str,
]:
    """Fixture with the read class, validator and the db item to read."""
    validator = ReadOperationValidation[ProviderBase, ProviderBasePublic, Provider](
        base=ProviderBase, base_public=ProviderBasePublic
    )
    return provider_mng, validator, db_provider_no_defaults, attr


@case(tags=["provider", "read_multi"])
@parametrize(attr=provider_get_attr)
def case_provider_read_items_actors(
    db_provider_simple: Provider, db_provider_no_defaults: Provider, attr: str
) -> Tuple[
    CRUDProvider,
    ReadOperationValidation[ProviderBase, ProviderBasePublic, Provider],
    Provider,
    str,
]:
    """Fixture with the read class, validator and the db items to read."""
    validator = ReadOperationValidation[ProviderBase, ProviderBasePublic, Provider](
        base=ProviderBase, base_public=ProviderBasePublic
    )
    return (
        provider_mng,
        validator,
        [db_provider_no_defaults, db_provider_simple],
        attr,
    )


@case(tags=["provider", "sort"])
@parametrize(reverse=[True, False])
@parametrize(attr=provider_sort_attr)
def case_provider_read_items_sort(
    db_provider_simple: Provider,
    db_provider_no_defaults: Provider,
    reverse: bool,
    attr: str,
) -> Tuple[
    CRUDProvider,
    ReadOperationValidation[ProviderBase, ProviderBasePublic, Provider],
    Provider,
    str,
]:
    """Fixture with the read class, validator and the db item to read."""
    validator = ReadOperationValidation[ProviderBase, ProviderBasePublic, Provider](
        base=ProviderBase, base_public=ProviderBasePublic
    )
    if reverse:
        attr = "-" + attr
    return (
        provider_mng,
        validator,
        [db_provider_no_defaults, db_provider_simple],
        attr,
    )


@case(tags=["provider", "skip"])
@parametrize(skip=[0, 1, 2])
def case_provider_read_items_skip(
    db_provider_simple: Provider, db_provider_no_defaults: Provider, skip: int
) -> Tuple[
    CRUDProvider,
    ReadOperationValidation[ProviderBase, ProviderBasePublic, Provider],
    Provider,
    str,
]:
    """Fixture with the read class, validator and the db item to read."""
    validator = ReadOperationValidation[ProviderBase, ProviderBasePublic, Provider](
        base=ProviderBase, base_public=ProviderBasePublic
    )
    return (
        provider_mng,
        validator,
        [db_provider_no_defaults, db_provider_simple],
        skip,
    )


@case(tags=["provider", "limit"])
@parametrize(limit=[None, 0, 1, 2, 3])
def case_provider_read_items_limit(
    db_provider_simple: Provider,
    db_provider_no_defaults: Provider,
    limit: Optional[int],
) -> Tuple[
    CRUDProvider,
    ReadOperationValidation[ProviderBase, ProviderBasePublic, Provider],
    Provider,
    str,
]:
    """Fixture with the read class, validator and the db item to read."""
    validator = ReadOperationValidation[ProviderBase, ProviderBasePublic, Provider](
        base=ProviderBase, base_public=ProviderBasePublic
    )
    return (
        provider_mng,
        validator,
        [db_provider_no_defaults, db_provider_simple],
        limit,
    )


@case(tags=["provider", "delete"])
def case_provider_delete_item_actors(
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


@case(tags=["provider", "patch"])
def case_provider_patch_item_actors(
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
    new_data = provider_patch_not_equal_data(
        db_item=db_provider_simple, new_data=provider_patch_valid_data
    )
    return provider_mng, validator, db_provider_simple, ProviderUpdate(**new_data)


@case(tags=["provider", "patch"])
@parametrize(attr=provider_patch_default_attr)
def case_provider_patch_item_with_default_actors(
    db_provider_no_defaults: Provider, attr: str
) -> Tuple[CRUDProvider, Provider, ProviderUpdate]:
    """Fixture with the delete class, validator and the db items to read."""
    validator = PatchOperationValidation[ProviderBase, ProviderBasePublic, Provider](
        base=ProviderBase, base_public=ProviderBasePublic
    )
    field_data = ProviderUpdate.__fields__.get(attr)
    provider_patch_valid_data = {attr: field_data.get_default()}
    return (
        provider_mng,
        validator,
        db_provider_no_defaults,
        ProviderUpdate(**provider_patch_valid_data),
    )


@case(tags=["provider", "patch_required_with_none"])
@parametrize(attr=provider_patch_required_attr)
def case_provider_patch_item_required_with_none_actors(
    db_provider_no_defaults: Provider, attr: str
) -> Tuple[CRUDProvider, Provider, ProviderUpdate]:
    """Fixture with the delete class, validator and the db items to read."""
    field_data = ProviderUpdate.__fields__.get(attr)
    provider_patch_valid_data = {attr: field_data.get_default()}
    return (
        provider_mng,
        db_provider_no_defaults,
        ProviderUpdate(**provider_patch_valid_data),
    )


@case(tags=["provider", "patch_no_changes"])
@parametrize(attr=provider_patch_attr)
def case_provider_patch_item_no_changes_actors(
    db_provider_simple: Provider, attr: str
) -> Tuple[CRUDProvider, Provider, ProviderUpdate]:
    """Fixture with the delete class, validator and the db items to read."""
    provider_patch_valid_data = {attr: db_provider_simple.__getattribute__(attr)}
    return (
        provider_mng,
        db_provider_simple,
        ProviderUpdate(**provider_patch_valid_data),
    )


@case(tags=["provider", "force_update"])
def case_provider_force_update_unchanged_rel_actors(
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


@case(tags=["provider", "force_update"])
@parametrize(start_empty=[True, False])
def case_provider_force_update_add_rel_actors(
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
        new_data = provider_create_with_rel
    else:
        new_data = provider_force_update_enriched_relationships_data(
            provider_create_with_rel
        )
        starting_data = provider_create_with_rel
    db_item = provider_mng.create(obj_in=ProviderCreateExtended(**starting_data))
    return provider_mng, validator, db_item, ProviderCreateExtended(**new_data)


@case(tags=["provider", "force_update"])
@parametrize(end_empty=[True, False])
def case_provider_force_update_remove_rel_actors(
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
        new_data = {
            **copy.deepcopy(provider_create_with_rel),
            "identity_providers": [],
            "projects": [],
            "regions": [],
        }
        starting_data = provider_create_with_rel
    else:
        starting_data = provider_force_update_enriched_relationships_data(
            provider_create_with_rel
        )
        new_data = provider_create_with_rel
    db_item = provider_mng.create(obj_in=ProviderCreateExtended(**starting_data))
    return provider_mng, validator, db_item, ProviderCreateExtended(**new_data)


@case(tags=["provider", "force_update"])
@parametrize(replace_all=[True, False])
def case_provider_force_update_replace_rel_actors(
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
        starting_data = provider_force_update_enriched_relationships_data(
            provider_create_with_rel
        )
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
