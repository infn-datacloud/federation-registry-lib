"""IdentityService specific cases."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import case, parametrize

from app.provider.schemas_extended import (
    IdentityServiceCreate,
)
from app.service.models import IdentityService
from app.service.schemas import (
    IdentityServiceBase,
    IdentityServiceRead,
    IdentityServiceReadPublic,
    IdentityServiceUpdate,
    ServiceBase,
)
from app.service.schemas_extended import (
    IdentityServiceReadExtended,
    IdentityServiceReadExtendedPublic,
)
from tests.common.schemas.validators import (
    CreateSchemaValidation,
    PatchSchemaValidation,
    ReadSchemaValidation,
)
from tests.common.utils import detect_public_extended_details


@case(tags="create_valid")
def case_identity_service_create_valid_schema_actors(
    identity_service_create_valid_data: Dict[str, Any],
) -> Tuple[
    Type[IdentityServiceCreate],
    CreateSchemaValidation[
        IdentityServiceBase,
        ServiceBase,
        IdentityServiceCreate,
    ],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    validator = CreateSchemaValidation[
        IdentityServiceBase,
        ServiceBase,
        IdentityServiceCreate,
    ](
        base=IdentityServiceBase,
        base_public=ServiceBase,
        create=IdentityServiceCreate,
    )
    return IdentityServiceCreate, validator, identity_service_create_valid_data


@case(tags="create_invalid")
def case_identity_service_create_invalid_schema_actors(
    identity_service_create_invalid_data: Dict[str, Any],
) -> Tuple[Type[IdentityServiceCreate], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return IdentityServiceCreate, identity_service_create_invalid_data


@case(tags="patch_valid")
def case_identity_service_patch_valid_schema_actors(
    identity_service_patch_valid_data: Dict[str, Any],
) -> Tuple[
    Type[IdentityServiceUpdate],
    PatchSchemaValidation[IdentityServiceBase, ServiceBase],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    validator = PatchSchemaValidation[IdentityServiceBase, ServiceBase](
        base=IdentityServiceBase, base_public=ServiceBase
    )
    return IdentityServiceUpdate, validator, identity_service_patch_valid_data


@case(tags="patch_invalid")
def case_identity_service_patch_invalid_schema_actors(
    identity_service_patch_invalid_data: Dict[str, Any],
) -> Tuple[Type[IdentityServiceUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return IdentityServiceUpdate, identity_service_patch_invalid_data


@case(tags="read")
@parametrize(
    cls=[
        IdentityServiceRead,
        IdentityServiceReadExtended,
        IdentityServiceReadPublic,
        IdentityServiceReadExtendedPublic,
    ],
)
def case_identity_service_valid_read_schema_tuple(
    cls: Union[
        IdentityServiceRead,
        IdentityServiceReadPublic,
        IdentityServiceReadExtended,
        IdentityServiceReadExtendedPublic,
    ],
    db_identity_service: IdentityService,
) -> Tuple[
    Union[
        IdentityServiceRead,
        IdentityServiceReadPublic,
        IdentityServiceReadExtended,
        IdentityServiceReadExtendedPublic,
    ],
    ReadSchemaValidation[
        IdentityServiceBase,
        ServiceBase,
        IdentityServiceRead,
        IdentityServiceReadPublic,
        IdentityServiceReadExtended,
        IdentityServiceReadExtendedPublic,
        IdentityService,
    ],
    IdentityService,
]:
    """Fixture with the read class, validator and the db item to read."""
    validator = ReadSchemaValidation[
        IdentityServiceBase,
        ServiceBase,
        IdentityServiceRead,
        IdentityServiceReadPublic,
        IdentityServiceReadExtended,
        IdentityServiceReadExtendedPublic,
        IdentityService,
    ](
        base=IdentityServiceBase,
        base_public=ServiceBase,
        read=IdentityServiceRead,
        read_extended=IdentityServiceReadExtended,
    )
    is_public, is_extended = detect_public_extended_details(cls)
    return cls, validator, db_identity_service, is_public, is_extended
