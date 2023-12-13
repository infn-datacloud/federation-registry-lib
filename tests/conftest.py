"""File to set tests configuration parameters and common fixtures."""
from glob import glob
from typing import Generator

import pytest
from neomodel import clear_neo4j_database, db


def refactor(string: str) -> str:
    """Convert filesystem paths into python packages paths."""
    return string.replace("/", ".").replace("\\", ".").replace(".py", "")


pytest_plugins = [refactor(fixture) for fixture in glob("tests/fixtures/[!__]*.py")] + [
    refactor(fixture) for fixture in glob("tests/**/fixtures.py")
]

pytest.register_assert_rewrite("tests.utils")


# DB specific fixtures


@pytest.fixture
def setup_and_teardown_db() -> Generator:
    """Clear the db at the beginning and at the end of each operation."""
    clear_neo4j_database(db)
    yield
    clear_neo4j_database(db)
