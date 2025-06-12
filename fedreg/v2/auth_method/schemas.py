"""Pydantic models of the Provider - Identity Provider relationship."""

from typing import Annotated

from pydantic import BaseModel, Field

from fedreg.v2.core import BaseNodeRead
from fedreg.v2.identity_provider.schemas import IdentityProviderBase


class OsAuthMethodCreate(BaseModel):
    """Schema with the parameters needed by authentication method for openstack.

    Attributes:
        idp_name (str): Identity Provider name saved in the Resource Provider.
        protocol (str): Protocol to use when authenticating on this identity provider
    """

    idp_name: Annotated[
        str, Field(description="Identity Provider name saved in the Resource Provider.")
    ]
    protocol: Annotated[
        str, Field(description="Protocol to use when authenticating on target IdP.")
    ]


class K8sAuthMethodCreate(BaseModel):
    """Schema with the parameters needed by authentication method for k8s clustes.

    Attributes:
        audience (str): Audience to use when authenticating on this identity provider.
    """

    audience: Annotated[
        str, Field(description="Audience to use when authenticating on target IdP.")
    ]


class AuthMethodRead(BaseNodeRead, IdentityProviderBase):
    """Represents a read-only schema for authentication methods

    Combines base node read attributes and identity provider base information.

    Inherits from:
        BaseNodeRead: Provides base attributes for node reading operations.
        IdentityProviderBase: Supplies identity provider-specific fields.

    Attributes:
        Inherits all attributes from BaseNodeRead and IdentityProviderBase.
    """
