import copy
from uuid import uuid4

import pytest
from app.tests.utils.provider import create_random_provider
from app.tests.utils.utils import random_url
from pydantic import ValidationError


def test_create_schema():
    create_random_provider()
    create_random_provider(default=True)
    create_random_provider(with_identity_providers=True)
    create_random_provider(default=True, with_identity_providers=True)
    create_random_provider(with_projects=True)
    create_random_provider(default=True, with_projects=True)
    create_random_provider(with_regions=True)
    create_random_provider(default=True, with_regions=True)
    create_random_provider(
        with_identity_providers=True, with_projects=True, with_regions=True
    )


def test_invalid_create_schema():
    a = create_random_provider(
        with_identity_providers=True, with_projects=True, with_regions=True
    )
    with pytest.raises(ValidationError):
        a.name = None
    with pytest.raises(ValidationError):
        a.type = None
    with pytest.raises(ValidationError):
        a.status = None
    with pytest.raises(ValidationError):
        a.identity_providers = [a.identity_providers[0], a.identity_providers[0]]
    with pytest.raises(ValidationError):
        a.projects = [a.projects[0], a.projects[0]]
    with pytest.raises(ValidationError):
        a.regions = [a.regions[0], a.regions[0]]
    with pytest.raises(ValidationError):
        idp1 = a.identity_providers[0]
        idp2 = copy.deepcopy(idp1)
        idp2.endpoint = random_url()
        a.identity_providers = [idp1, idp2]
    with pytest.raises(ValidationError):
        idp = a.identity_providers[0]
        idp.user_groups[0].slas[0].projects = [uuid4()]
        a.identity_providers = [idp]
    with pytest.raises(ValidationError):
        reg = a.regions[0]
        reg.block_storage_services[0].quotas[0].project = uuid4()
        a.regions = [reg]
    with pytest.raises(ValidationError):
        reg = a.regions[0]
        reg.compute_services[0].flavors[0].projects = [uuid4()]
        a.regions = [reg]
    with pytest.raises(ValidationError):
        reg = a.regions[0]
        reg.compute_services[0].images[0].projects = [uuid4()]
        a.regions = [reg]
    with pytest.raises(ValidationError):
        reg = a.regions[0]
        reg.compute_services[0].quotas[0].project = uuid4()
        a.regions = [reg]
    with pytest.raises(ValidationError):
        reg = a.regions[0]
        reg.network_services[0].networks[0].project = uuid4()
        a.regions = [reg]
