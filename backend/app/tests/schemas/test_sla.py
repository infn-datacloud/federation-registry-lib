from datetime import timedelta
from uuid import uuid4

import pytest
from app.tests.utils.sla import create_random_sla
from pydantic import ValidationError


def test_create_schema():
    projects = [uuid4()]
    create_random_sla(projects=projects)
    create_random_sla(default=True, projects=projects)


def test_invalid_create_schema():
    a = create_random_sla(projects=[uuid4()])
    with pytest.raises(ValidationError):
        a.doc_uuid = None
    with pytest.raises(ValidationError):
        a.start_date = a.end_date
    with pytest.raises(ValidationError):
        a.end_date = a.start_date - timedelta(1)
    with pytest.raises(ValidationError):
        a.projects = [a.projects[0], a.projects[0]]
