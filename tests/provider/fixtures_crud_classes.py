"""Provider specific fixtures."""
from pytest_cases import fixture

from app.identity_provider.crud import identity_provider_mng
from app.project.crud import project_mng
from app.provider.crud import CRUDProvider, provider_mng
from app.provider.models import Provider
from app.provider.schemas import ProviderBase, ProviderBasePublic
from app.provider.schemas_extended import ProviderCreateExtended
from app.region.crud import region_mng
from tests.common.crud.validators import (
    CreateOperationValidation,
    DeleteOperationValidation,
    ReadOperationValidation,
)


@fixture
def provider_create_operation_validator() -> (
    CreateOperationValidation[
        ProviderBase, ProviderBasePublic, ProviderCreateExtended, Provider
    ]
):
    """Instance to validate provider create schemas."""
    return CreateOperationValidation[
        ProviderBase, ProviderBasePublic, ProviderCreateExtended, Provider
    ](base=ProviderBase, base_public=ProviderBasePublic, create=ProviderCreateExtended)


@fixture
def provider_read_operation_validator() -> (
    ReadOperationValidation[ProviderBase, ProviderBasePublic, Provider]
):
    """Instance to validate provider read schemas."""
    return ReadOperationValidation[ProviderBase, ProviderBasePublic, Provider](
        base=ProviderBase, base_public=ProviderBasePublic
    )


@fixture
def provider_delete_operation_validator() -> (
    DeleteOperationValidation[ProviderBase, ProviderBasePublic, Provider]
):
    """Instance to validate provider delete schemas."""
    return DeleteOperationValidation[ProviderBase, ProviderBasePublic, Provider](
        base=ProviderBase,
        base_public=ProviderBasePublic,
        managers={
            "identity_providers": identity_provider_mng,
            "projects": project_mng,
            "regions": region_mng,
        },
    )


@fixture
def provider_manager() -> CRUDProvider:
    """Return provider manager."""
    return provider_mng
