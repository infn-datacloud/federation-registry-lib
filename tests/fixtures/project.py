import pytest

from app.project.crud import project
from app.project.models import Project
from app.provider.models import Provider
from tests.utils.project import create_random_project


@pytest.fixture
def db_project(db_provider: Provider) -> Project:
    """Project owned by first provider."""
    item_in = create_random_project()
    db_project = project.create(obj_in=item_in, provider=db_provider)
    yield db_project


@pytest.fixture
def db_project2(db_provider2: Provider) -> Project:
    """First project owned by second provider."""
    item_in = create_random_project()
    db_project = project.create(obj_in=item_in, provider=db_provider2)
    yield db_project


@pytest.fixture
def db_project3(db_project2: Project) -> Project:
    """Second project owned by second provider."""
    item_in = create_random_project()
    db_project = project.create(obj_in=item_in, provider=db_project2.provider.single())
    yield db_project


@pytest.fixture
def db_provider_with_single_project(db_project: Project) -> Provider:
    """Provider with a single project."""
    yield db_project.provider.single()


@pytest.fixture
def db_provider_with_multiple_projects(db_project3: Project) -> Provider:
    """Provider with multiple (2) projects."""
    yield db_project3.provider.single()
