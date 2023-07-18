import requests
from fastapi import status
from app.flavor.schemas import FlavorCreate
from app.service.enum import ServiceType
from app.service.schemas import NovaServiceCreate, NovaServiceRead, ServiceCreate, ServiceRead
from app.tests.utils.utils import random_int, random_lower_string, random_url

print(NovaServiceRead.__config__.extra)
exit()

data = {
    "name": f"provider{random_int()}",
    "services": [
        {
            "type": ServiceType.openstack_nova.value,
            "endpoint": "http://" + random_lower_string(),
            "myfield": 1,
        }
    ],
}
response = requests.post(
    f"http://localhost:8000/providers/",
    json=data,
    # headers=superuser_token_headers,
)
#assert response.status_code == status.HTTP_201_CREATED
content = response.json()
print(content)

#
# a = NovaService(endpoint="url")
#
# query = f"CREATE (n:{':'.join(NovaService.inherited_labels())} $create_params)"
# db.cypher_query(query, {"create_params": a.dict()})
