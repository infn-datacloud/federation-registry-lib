from uuid import uuid4

import pytest
from app.tests.utils.identity_provider import create_random_identity_provider
from pydantic import ValidationError


def test_create_schema():
    create_random_identity_provider()
    create_random_identity_provider(default=True)


def test_invalid_create_schema():
    projects = [uuid4()]
    a = create_random_identity_provider(projects=projects)
    with pytest.raises(ValidationError):
        a.endpoint = None
    with pytest.raises(ValidationError):
        a.group_claim = None
    with pytest.raises(ValidationError):
        a.relationship = None
    with pytest.raises(ValidationError):
        a.user_groups = [a.user_groups[0], a.user_groups[0]]
