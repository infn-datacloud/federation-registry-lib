from providers.opnstk import get_os_provider
from utils import choose_idp, generate_token, load_config

if __name__ == "__main__":
    config = load_config()

    tokens = {}
    providers = []
    for conf in config.openstack:
        # At first, Choose which IDP should be used to authenticate script.
        # Generate a token using OIDC-Agent if not yet present.
        # Then retrieve Provider data.
        chosen_idp = choose_idp(conf.identity_providers)
        if tokens.get(chosen_idp.endpoint) is None:
            tokens[chosen_idp.endpoint] = generate_token(chosen_idp.endpoint)
        providers.append(
            get_os_provider(
                config=conf, chosen_idp=chosen_idp, token=tokens[chosen_idp.endpoint]
            )
        )

    cmdb_url = "http://localhost:8000"

#    resp = requests.post(
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
