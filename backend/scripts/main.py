import yaml
from providers.openstack import create_os_provider
from scripts.models import Config

if __name__ == "__main__":
    tokens = {}

    with open("config.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        config = Config(**config)

    for i in config.openstack:
        provider = create_os_provider(i, tokens)
        print(provider)

# print(provider)
# cmdb_url = "http://localhost:8000"

# print(conn.identity.projects())
# for project in conn.identity.projects():
#   print(project)

# resp = requests.post(
#    url=os.path.join(cmdb_url, "api/v1/providers/"),
#    data=provider,
#    headers={
#        "Authorization": "Bearer"
#    },
# )
# if resp.status_code != 201:
#    raise  # TODO
# print(resp.json())
#
# for service in conn.service_catalog:
#   print(service)
# for service in conn.list_services():
#    print(service)

# for image in conn.image.images():
# print(image)
#    print(image.to_dict().keys())
#    for k,v in image.to_dict().items():
#        print(f"{k}: {v}")
# for project in conn.identity.projects():
#    print(project)
# for idp in conn.identity.identity_providers():
#    print(idp)
