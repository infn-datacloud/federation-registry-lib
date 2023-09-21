from app.network.schemas import NetworkRead, NetworkReadPublic
from app.project.schemas import ProjectRead, ProjectReadPublic
from app.service.schemas import NetworkServiceRead, NetworkServiceReadPublic
from pydantic import Field


class NetworkReadExtended(NetworkRead):
    """Model to extend the Network data read from the DB with the lists of
    related items for authenticated users."""

    project: ProjectRead = Field(
        default_factory=list, description="List of accessible project"
    )
    service: NetworkServiceRead = Field(description="Network service")


class NetworkReadExtendedPublic(NetworkReadPublic):
    """Model to extend the Network data read from the DB with the lists of
    related items for non-authenticated users."""

    project: ProjectReadPublic = Field(
        default_factory=list, description="List of accessible project"
    )
    service: NetworkServiceReadPublic = Field(description="Network service")
