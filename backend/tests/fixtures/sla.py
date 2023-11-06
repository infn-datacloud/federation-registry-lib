import pytest
from app.project.models import Project
from app.sla.models import SLA
from app.user_group.models import UserGroup


@pytest.fixture
def db_sla(db_user_group: UserGroup) -> SLA:
    """SLA owned by the user group of the provider with just one project."""
    yield db_user_group.slas.single()


@pytest.fixture
def db_sla2(db_user_group2: UserGroup) -> SLA:
    """SLA owned by first user group of the provider with multiple projects."""
    yield db_user_group2.slas.single()


@pytest.fixture
def db_sla3(db_user_group3: UserGroup) -> SLA:
    """SLA owned by second user group of the provider with multiple projects."""
    yield db_user_group3.slas.single()


@pytest.fixture
def db_sla_with_multiple_projects(db_sla: SLA, db_project2: Project) -> SLA:
    db_sla.projects.connect(db_project2)
    assert len(db_sla.projects) == 2
    assert (
        db_sla.projects.all()[0].provider.single()
        != db_sla.projects.all()[1].provider.single()
    )
    yield db_sla


@pytest.fixture
def db_project_with_sla(db_sla: SLA) -> Project:
    """Project with a single SLA."""
    yield db_sla.projects.single()


@pytest.fixture
def db_project_with_shared_sla(db_sla_with_multiple_projects: SLA) -> Project:
    """Project with SLA shared between multiple projects."""
    yield db_sla_with_multiple_projects.projects.single()


@pytest.fixture
def db_user_group_with_sla_with_multiple_projects(
    db_sla_with_multiple_projects: SLA,
) -> UserGroup:
    """User group with an SLA pointing to multiple projects on different providers."""
    yield db_sla_with_multiple_projects.user_group.single()
