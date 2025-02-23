from typing import Any, Literal

from pytest_cases import case, parametrize_with_cases

from fedreg.auth_method.models import AuthMethod
from fedreg.auth_method.schemas import AuthMethodBase, AuthMethodCreate, AuthMethodRead
from fedreg.identity_provider.models import IdentityProvider
from fedreg.identity_provider.schemas import IdentityProviderBase
from fedreg.provider.models import Provider
from fedreg.provider.schemas import ProviderBase
from tests.schemas.utils import (
    auth_method_schema_dict,
    identity_provider_schema_dict,
    provider_schema_dict,
)


class CaseAuthMethodSchema:
    @case(tags=("dict", "valid"))
    def case_mandatory(self) -> dict[str, Any]:
        return auth_method_schema_dict()

    @case(tags=("dict", "invalid"))
    def case_missing_idp_name(self) -> tuple[dict[str, Any], Literal["idp_name"]]:
        d = auth_method_schema_dict()
        d.pop("idp_name")
        return d, "idp_name"

    @case(tags=("dict", "invalid"))
    def case_missing_protocol(self) -> tuple[dict[str, Any], Literal["protocol"]]:
        d = auth_method_schema_dict()
        d.pop("protocol")
        return d, "protocol"

    @case(tags="class")
    def case_base_class(self) -> type[AuthMethodBase]:
        return AuthMethodBase

    @case(tags="class")
    def case_create_class(self) -> type[AuthMethodCreate]:
        return AuthMethodCreate

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
            provider_model, AuthMethodBase(**data).dict()
        )
        return auth_method_model
