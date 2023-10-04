from datetime import timedelta

import pytest
from app.tests.utils.sla import create_random_sla
from pydantic import ValidationError


def test_create_schema():
    create_random_sla()
    create_random_sla(default=True)
    create_random_sla(with_projects=True)
    create_random_sla(default=True, with_projects=True)


def test_invalid_create_schema():
    a = create_random_sla(with_projects=True)
    with pytest.raises(ValidationError):
        a.doc_uuid = None
    with pytest.raises(ValidationError):
        a.start_date = a.end_date
    with pytest.raises(ValidationError):
        a.end_date = a.start_date - timedelta(1)
    with pytest.raises(ValidationError):
        a.projects = [a.projects[0], a.projects[0]]
