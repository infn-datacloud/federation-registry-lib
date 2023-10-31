import pytest
from app.sla.models import SLA
from app.user_group.models import UserGroup


@pytest.fixture
def db_sla(db_user_group: UserGroup) -> SLA:
    """SLA owned by the user group of the provider with just one project."""
    yield db_user_group.slas.all()[0]


@pytest.fixture
def db_sla2(db_user_group2: UserGroup) -> SLA:
    """SLA owned by first user group of the provider with multiple projects."""
    yield db_user_group2.slas.all()[0]


@pytest.fixture
def db_sla3(db_user_group3: UserGroup) -> SLA:
    """SLA owned by second user group of the provider with multiple
    projects."""
    yield db_user_group3.slas.all()[0]


# TODO Create SLA fixture with multiple projects of different providers
