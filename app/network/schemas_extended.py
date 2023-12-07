"""Pydantic extended models of the Virtual Machine Network owned by a Provider."""
from typing import Optional

from pydantic import Field

from app.network.constants import DOC_EXT_PROJ, DOC_EXT_SERV
from app.network.schemas import NetworkRead, NetworkReadPublic
from app.project.schemas import ProjectRead
from app.provider.schemas import ProviderRead, ProviderReadPublic
from app.region.constants import DOC_EXT_PROV
from app.region.schemas import RegionRead, RegionReadPublic
from app.service.constants import DOC_EXT_REG
from app.service.schemas import NetworkServiceRead, NetworkServiceReadPublic


class RegionReadExtended(RegionRead):
    """Model to extend the Region data read from the DB.

    Attributes:
    ----------
        uid (uuid): AssociatedRegion unique ID.
        description (str): Brief description.
        name (str): Name of the Region in the Provider.
        provider (ProviderRead): Provider hosting target region.
    """

    provider: ProviderRead = Field(description=DOC_EXT_PROV)


class RegionReadExtendedPublic(RegionReadPublic):
    """Model to extend the Region public data read from the DB.

    Attributes:
    ----------
        uid (uuid): AssociatedRegion unique ID.
        description (str): Brief description.
        name (str): Name of the Region in the Provider.
        provider (ProviderReadPublic): Provider hosting target region.
    """

    provider: ProviderReadPublic = Field(description=DOC_EXT_PROV)


class NetworkServiceReadExtended(NetworkServiceRead):
    """Model to extend the Network Service data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name.
        region (RegionReadExtended): Region hosting this service.
    """

    region: RegionReadExtended = Field(description=DOC_EXT_REG)


class NetworkServiceReadExtendedPublic(NetworkServiceReadPublic):
    """Model to extend the Network Service public data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        region (RegionReadExtendedPublic): Region hosting this service.
    """

    region: RegionReadExtendedPublic = Field(description=DOC_EXT_REG)


class NetworkReadExtended(NetworkRead):
    """Model to extend the Network data read from the DB.

    uid (int): Network unique ID.
        description (str): Brief description.
        name (str): Network name in the Provider.
        uuid (str): Network unique ID in the Provider
        is_shared (bool): Public or private Network.
        is_router_external (bool): Network with access to the outside.
        is_default (bool): Network to use as default.
        mtu (int | None): Metric transmission unit (B).
        proxy_ip (str | None): Proxy IP address.
        proxy_user (str | None): Proxy username.
        tags (list of str): List of tags associated to this Network.
        project (ProjectRead | None): Project having access to this network if the
            network is not shared.
        service (NetworkServiceReadExtended): Network Service supplying this network.
    """

    project: Optional[ProjectRead] = Field(default=None, description=DOC_EXT_PROJ)
    service: NetworkServiceReadExtended = Field(description=DOC_EXT_SERV)


class NetworkReadExtendedPublic(NetworkReadPublic):
    """Model to extend the Network public data read from the DB.

    uid (int): Network unique ID.
        description (str): Brief description.
        name (str): Network name in the Provider.
        uuid (str): Network unique ID in the Provider
        project (ProjectRead | None): Projects having access to this network if the
            network is not shared.
        service (NetworkServiceReadExtendedPublic): Network Service supplying this
            network.
    """

    project: Optional[ProjectRead] = Field(default=None, description=DOC_EXT_PROJ)
    service: NetworkServiceReadExtendedPublic = Field(description=DOC_EXT_SERV)
