from cmdb import add_or_patch_provider
from providers.opnstk import get_os_provider
from utils import build_cmdb_urls, choose_idp, generate_token, load_config

if __name__ == "__main__":
    config = load_config()
    cmdb_urls = build_cmdb_urls(config=config)

    tokens = {}
    providers = []
    for conf in config.openstack:
        # At first, Choose which IDP should be used to authenticate script.
        # Generate a token using OIDC-Agent if not yet present.
        # Then retrieve Provider data.
        chosen_idp = choose_idp(
            identity_providers=conf.identity_providers,
            preferred_idp_list=config.oidc_agent_accounts,
        )
        if tokens.get(chosen_idp.endpoint) is None:
            tokens[chosen_idp.endpoint] = generate_token(endpoint=chosen_idp.endpoint)

        provider = get_os_provider(
            config=conf, chosen_idp=chosen_idp, token=tokens[chosen_idp.endpoint]
        )
        providers.append(provider)

    for provider in providers:
        add_or_patch_provider(
            cmdb_urls=cmdb_urls, provider=provider, token=tokens[chosen_idp.endpoint]
        )
