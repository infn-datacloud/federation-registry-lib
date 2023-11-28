from typing import Generator

import pytest

from app.provider.crud import provider
from app.provider.models import Provider
from tests.utils.provider import create_random_provider


@pytest.fixture
def db_provider(setup_and_teardown_db: Generator) -> Provider:
    """First Provider with no relationships."""
    item_in = create_random_provider()
    item = provider.create(obj_in=item_in)
    yield item


@pytest.fixture
def db_provider2(setup_and_teardown_db: Generator) -> Provider:
    """Second Provider with no relationships."""
    item_in = create_random_provider()
    item = provider.create(obj_in=item_in)
    yield item


@pytest.fixture
def db_provider3(db_provider2: Provider) -> Provider:
    """Third Provider with no relationships."""
    item_in = create_random_provider()
    item = provider.create(obj_in=item_in)
    yield item
