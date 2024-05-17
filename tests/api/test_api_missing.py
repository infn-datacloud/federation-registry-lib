from uuid import uuid4

from fastapi import status
from pytest_cases import case, parametrize, parametrize_with_cases


class CaseItemNameEndpoint:
    @parametrize(
        **{
            "item, endpoint": [
                ("Flavor", "flavors"),
                ("Identity Provider", "identity_providers"),
                ("Image", "images"),
                ("Location", "locations"),
                ("Network", "networks"),
                ("Project", "projects"),
                ("Provider", "providers"),
                ("Block Storage Quota", "block_storage_quotas"),
                ("Compute Quota", "compute_quotas"),
                ("Network Quota", "network_quotas"),
                ("Object Storage Quota", "object_storage_quotas"),
                ("Region", "regions"),
                ("Block Storage Service", "block_storage_services"),
                ("Compute Service", "compute_services"),
                ("Identity Service", "identity_services"),
                ("Network Service", "network_services"),
                ("Object Storage Service", "object_storage_services"),
                ("SLA", "slas"),
                ("User Group", "user_groups"),
            ]
        }
    )
    def case_item_endpoint(self, item: str, endpoint: str) -> tuple[str, str]:
        return item, endpoint

    @case(tags=["provider"])
    def case_provider(self) -> tuple[str, str]:
        return "Provider", "providers"


@parametrize_with_cases("item, endpoint", cases=CaseItemNameEndpoint)
def test_get_missing(client_no_authn, item: str, endpoint: str):
    uid = uuid4()
    resp = client_no_authn.get(f"/api/v1/{endpoint}/{uid}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert resp.json().get("detail") == f"{item} '{uid}' not found"


@parametrize_with_cases("item, endpoint", cases=CaseItemNameEndpoint)
def test_patch_missing(client_no_authn, item: str, endpoint: str):
    uid = uuid4()
    resp = client_no_authn.patch(f"/api/v1/{endpoint}/{uid}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert resp.json().get("detail") == f"{item} '{uid}' not found"


@parametrize_with_cases(
    "item, endpoint", cases=CaseItemNameEndpoint, has_tag="provider"
)
def test_put_missing(client_no_authn, item: str, endpoint: str):
    uid = uuid4()
    resp = client_no_authn.put(f"/api/v1/{endpoint}/{uid}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert resp.json().get("detail") == f"{item} '{uid}' not found"


@parametrize_with_cases("item, endpoint", cases=CaseItemNameEndpoint)
def test_delete_missing(client_no_authn, item: str, endpoint: str):
    uid = uuid4()
    resp = client_no_authn.delete(f"/api/v1/{endpoint}/{uid}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert resp.json().get("detail") == f"{item} '{uid}' not found"


@parametrize_with_cases("item, endpoint", cases=CaseItemNameEndpoint)
def test_get_multi_empty(client_no_authn, item: str, endpoint: str):
    resp = client_no_authn.get(f"/api/v1/{endpoint}/")
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.json()) == 0
