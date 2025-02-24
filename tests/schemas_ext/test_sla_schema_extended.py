import pytest
from neomodel.exceptions import CardinalityViolation
from pytest_cases import parametrize_with_cases

from fedreg.core import BaseReadPrivateExtended, BaseReadPublicExtended
from fedreg.identity_provider.models import IdentityProvider
from fedreg.identity_provider.schemas import (
    IdentityProviderRead,
    IdentityProviderReadPublic,
)
from fedreg.project.models import Project
from fedreg.project.schemas import ProjectRead, ProjectReadPublic
from fedreg.provider.models import Provider
from fedreg.provider.schemas import ProviderRead, ProviderReadPublic
from fedreg.sla.models import SLA
from fedreg.sla.schemas import SLARead, SLAReadPublic
from fedreg.sla.schemas_extended import (
    ProjectReadExtended,
    ProjectReadExtendedPublic,
    SLAReadExtended,
    SLAReadExtendedPublic,
    UserGroupReadExtended,
    UserGroupReadExtendedPublic,
)
from fedreg.user_group.models import UserGroup
from fedreg.user_group.schemas import UserGroupRead, UserGroupReadPublic


def test_class_inheritance():
    assert issubclass(SLAReadExtended, BaseReadPrivateExtended)
    assert issubclass(SLAReadExtended, SLARead)
    assert SLAReadExtended.__fields__["schema_type"].default == "private_extended"
    assert SLAReadExtended.__config__.orm_mode is True

    assert issubclass(SLAReadExtendedPublic, BaseReadPublicExtended)
    assert issubclass(SLAReadExtendedPublic, SLAReadPublic)
    assert SLAReadExtendedPublic.__fields__["schema_type"].default == "public_extended"
    assert SLAReadExtendedPublic.__config__.orm_mode is True

    assert issubclass(UserGroupReadExtended, UserGroupRead)
    assert issubclass(UserGroupReadExtendedPublic, UserGroupReadPublic)

    assert issubclass(ProjectReadExtended, ProjectRead)
    assert issubclass(ProjectReadExtendedPublic, ProjectReadPublic)


@parametrize_with_cases("projects", has_tag="projects")
def test_read_ext(
    sla_model: SLA,
    user_group_model: UserGroup,
    identity_provider_model: IdentityProvider,
    projects: list[Project],
) -> None:
    identity_provider_model.user_groups.connect(user_group_model)
    sla_model.user_group.connect(user_group_model)
    for project in projects:
        sla_model.projects.connect(project)

    item = SLAReadExtendedPublic.from_orm(sla_model)
    assert item.user_group is not None
    assert item.user_group == UserGroupReadExtendedPublic.from_orm(user_group_model)
    assert len(item.projects) == len(projects)

    item = SLAReadExtended.from_orm(sla_model)
    assert item.user_group is not None
    assert item.user_group == UserGroupReadExtended.from_orm(user_group_model)
    assert len(item.projects) == len(projects)


def test_user_group_read_ext(
    identity_provider_model: IdentityProvider, user_group_model: UserGroup
):
    with pytest.raises(CardinalityViolation):
        UserGroupReadExtended.from_orm(user_group_model)
    identity_provider_model.user_groups.connect(user_group_model)
    user_group = UserGroupReadExtended.from_orm(user_group_model)
    assert user_group.identity_provider == IdentityProviderRead.from_orm(
        identity_provider_model
    )


def test_user_group_read_ext_public(
    identity_provider_model: IdentityProvider, user_group_model: UserGroup
):
    with pytest.raises(CardinalityViolation):
        UserGroupReadExtendedPublic.from_orm(user_group_model)
    identity_provider_model.user_groups.connect(user_group_model)
    user_group = UserGroupReadExtendedPublic.from_orm(user_group_model)
    assert user_group.identity_provider == IdentityProviderReadPublic.from_orm(
        identity_provider_model
    )


def test_project_read_ext(provider_model: Provider, project_model: Project):
    with pytest.raises(CardinalityViolation):
        ProjectReadExtended.from_orm(project_model)
    provider_model.projects.connect(project_model)
    project = ProjectReadExtended.from_orm(project_model)
    assert project.provider == ProviderRead.from_orm(provider_model)


def test_project_read_ext_public(provider_model: Provider, project_model: Project):
    with pytest.raises(CardinalityViolation):
        ProjectReadExtendedPublic.from_orm(project_model)
    provider_model.projects.connect(project_model)
    project = ProjectReadExtendedPublic.from_orm(project_model)
    assert project.provider == ProviderReadPublic.from_orm(provider_model)
