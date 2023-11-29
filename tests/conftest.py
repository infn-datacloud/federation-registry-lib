from glob import glob
from typing import Generator

import pytest
from neomodel import clear_neo4j_database, db


def refactor(string: str) -> str:
    return string.replace("/", ".").replace("\\", ".").replace(".py", "")


pytest_plugins = [refactor(fixture) for fixture in glob("tests/fixtures/[!__]*.py")] + [
    refactor(fixture) for fixture in glob("tests/flavor/fixtures.py")
]

pytest.register_assert_rewrite("tests.utils")


# DB specific fixtures


@pytest.fixture
def setup_and_teardown_db() -> Generator:
    clear_neo4j_database(db)
    yield
    clear_neo4j_database(db)
