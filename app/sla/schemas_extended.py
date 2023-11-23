from typing import List, Union

from pydantic import Field

from app.identity_provider.schemas import (
    IdentityProviderRead,
    IdentityProviderReadPublic,
)
from app.project.schemas import ProjectRead, ProjectReadPublic
from app.provider.schemas import ProviderRead, ProviderReadPublic
from app.quota.schemas import (
    BlockStorageQuotaRead,
    BlockStorageQuotaReadPublic,
    ComputeQuotaRead,
    ComputeQuotaReadPublic,
)
from app.service.schemas import (
    BlockStorageServiceRead,
    BlockStorageServiceReadPublic,
    ComputeServiceRead,
    ComputeServiceReadPublic,
)
from app.sla.schemas import SLARead, SLAReadPublic
from app.user_group.schemas import UserGroupRead, UserGroupReadPublic


class BlockStorageQuotaReadExtended(BlockStorageQuotaRead):
    service: BlockStorageServiceRead


class BlockStorageQuotaReadExtendedPublic(BlockStorageQuotaReadPublic):
    service: BlockStorageServiceReadPublic


class ComputeQuotaReadExtended(ComputeQuotaRead):
    service: ComputeServiceRead


class ComputeQuotaReadExtendedPublic(ComputeQuotaReadPublic):
    service: ComputeServiceReadPublic


class ProjectReadExtended(ProjectRead):
    """Model to extend the Project data read from the DB with the lists of related
    items.
    """

    provider: ProviderRead = Field(description="Provider owning this project")
    quotas: List[
        Union[BlockStorageQuotaReadExtended, ComputeQuotaReadExtended]
    ] = Field(
        description="List of quotas owned by this Project.",
    )


class ProjectReadExtendedPublic(ProjectReadPublic):
    """Model to extend the Project data read from the DB with the lists of related
    items.
    """

    provider: ProviderReadPublic = Field(description="Provider owning this project")
    quotas: List[
        Union[BlockStorageQuotaReadExtendedPublic, ComputeQuotaReadExtendedPublic]
    ] = Field(
        description="List of quotas owned by this Project.",
    )


class UserGroupReadExtended(UserGroupRead):
    """Model to extend the User Group data read from the DB with the lists of related
    items.
    """

    identity_provider: IdentityProviderRead = Field(
        description="Identity Provider owning this User Group."
    )


class UserGroupReadExtendedPublic(UserGroupReadPublic):
    """Model to extend the User Group data read from the DB with the lists of related
    items.
    """

    identity_provider: IdentityProviderReadPublic = Field(
        description="Identity Provider owning this User Group."
    )


class SLAReadExtended(SLARead):
    """Model to extend the SLA data read from the DB with the lists of related items for
    authenticated users.
    """

    projects: List[ProjectReadExtended] = Field(description="Involved Projects.")
    user_group: UserGroupReadExtended = Field(description="Involved User Group.")


class SLAReadExtendedPublic(SLAReadPublic):
    """Model to extend the SLA data read from the DB with the lists of related items for
    non-authenticated users.
    """

    projects: List[ProjectReadExtendedPublic] = Field(description="Involved Projects.")
    user_group: UserGroupReadExtendedPublic = Field(description="Involved User Group.")
