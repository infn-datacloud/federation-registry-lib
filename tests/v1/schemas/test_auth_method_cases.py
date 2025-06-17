from typing import Any

from pytest_cases import case, parametrize_with_cases

from fedreg.v1.auth_method.models import AuthMethod
from fedreg.v1.auth_method.schemas import AuthMethodRead, OsAuthMethodCreate
from fedreg.v1.identity_provider.models import IdentityProvider
from fedreg.v1.identity_provider.schemas import IdentityProviderBase
from fedreg.v1.provider.models import Provider
from fedreg.v1.provider.schemas import ProviderBase
from tests.v1.schemas.utils import (
    auth_method_schema_dict,
    identity_provider_schema_dict,
    provider_schema_dict,
)


class CaseAuthMethodSchema:
    @case(tags=("dict", "valid"))
    def case_mandatory(self) -> dict[str, Any]:
        return auth_method_schema_dict()

    @case(tags="class")
    def case_base_class(self) -> type[OsAuthMethodCreate]:
        return OsAuthMethodCreate

    @case(tags="class")
    def case_create_class(self) -> type[OsAuthMethodCreate]:
        return OsAuthMethodCreate

    @case(tags="class")
    def case_read_class(self) -> type[AuthMethodRead]:
        return AuthMethodRead


class CaseAuthMethodModel:
    @case(tags="model")
    @parametrize_with_cases(
        "data", cases=CaseAuthMethodSchema, has_tag=("dict", "valid")
    )
    def case_auth_method_model(self, data: dict[str, Any]) -> AuthMethod:
        identity_provider_model = IdentityProvider(
            **IdentityProviderBase(**identity_provider_schema_dict()).dict()
        ).save()
        provider_model = Provider(
            **ProviderBase(**provider_schema_dict()).dict()
        ).save()
        auth_method_model = identity_provider_model.providers.connect(
            provider_model, OsAuthMethodCreate(**data).dict()
        )
        return auth_method_model
