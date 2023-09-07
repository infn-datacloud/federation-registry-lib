from cmdb import add_or_patch_provider
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
    for provider in providers:
        add_or_patch_provider(
            url=cmdb_url, provider=provider, token=tokens[chosen_idp.endpoint]
        )
