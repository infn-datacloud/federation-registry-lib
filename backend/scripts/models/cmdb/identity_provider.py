from app.identity_provider.schemas import IdentityProviderQuery
from app.identity_provider.schemas_extended import IdentityProviderReadExtended
from app.provider.schemas_extended import (
    AuthMethodCreate,
    IdentityProviderCreateExtended,
)
from pydantic import BaseModel


class Representation(BaseModel):
    def __str__(self) -> str:
        return f"{self.endpoint}"


class IdentityProviderWrite(IdentityProviderCreateExtended, Representation):
    pass


class IdentityProviderRead(IdentityProviderReadExtended, Representation):
    pass


class IdentityProviderQuery(IdentityProviderQuery, Representation):
    pass


class AuthMethodWrite(AuthMethodCreate):
    pass
