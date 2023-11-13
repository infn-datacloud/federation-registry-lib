from typing import Generator

import pytest

from app.provider.crud import provider
from app.provider.models import Provider
from tests.utils.provider import create_random_provider, random_type


@pytest.fixture
def db_provider(setup_and_teardown_db: Generator) -> Provider:
    """First Provider with no relationships."""
    item_in = create_random_provider()
    item = provider.create(obj_in=item_in)
    yield item


@pytest.fixture
def db_provider2(db_provider: Provider) -> Provider:
    """Second Provider with no relationships.

    If the first is public, this is private. It has the same type as the first one.
    """
    item_in = create_random_provider()
    item_in.is_public = not db_provider.is_public
    item_in.type = db_provider.type
    item = provider.create(obj_in=item_in)
    yield item


@pytest.fixture
def db_provider3(db_provider2: Provider) -> Provider:
    """Third Provider with no relationships.

    It has a different type from the other two providers.
    """
    item_in = create_random_provider()
    while item_in.type == item_in.type:
        item_in.type = random_type()
    item = provider.create(obj_in=item_in)
    yield item
