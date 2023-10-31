import pytest
from app.provider.models import Provider
from app.region.crud import region
from app.region.models import Region
from tests.utils.region import create_random_region


@pytest.fixture
def db_region(db_provider_with_single_project: Provider) -> Region:
    """Region owned by provider with a single project."""
    item_in = create_random_region()
    item = region.create(obj_in=item_in, provider=db_provider_with_single_project)
    yield item


@pytest.fixture
def db_region2(db_provider_with_multiple_projects: Provider) -> Region:
    """First region owned by the provider with multiple regions."""
    item_in = create_random_region()
    item = region.create(obj_in=item_in, provider=db_provider_with_multiple_projects)
    yield item


@pytest.fixture
def db_region3(db_region2: Region) -> Region:
    """Second region owned by the provider with multiple regions."""
    item_in = create_random_region()
    item = region.create(obj_in=item_in, provider=db_region2.provider.single())
    yield item


@pytest.fixture
def db_provider_with_single_region(db_region: Region) -> Provider:
    """Provider with single region."""
    yield db_region.provider.single()


@pytest.fixture
def db_provider_with_multiple_regions(db_region3: Region) -> Provider:
    """Provider with multiple regions."""
    yield db_region3.provider.single()
