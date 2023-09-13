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
            url=config.cmdb.url,
            provider=provider,
            token=tokens[chosen_idp.endpoint],
            api_ver_providers=config.cmdb.api_ver_providers,
            api_ver_projects=config.cmdb.api_ver_projects,
            api_ver_locations=config.cmdb.api_ver_locations,
            api_ver_flavors=config.cmdb.api_ver_flavors,
            api_ver_images=config.cmdb.api_ver_images,
            api_ver_identity_providers=config.cmdb.api_ver_identity_providers,
            api_ver_quotas=config.cmdb.api_ver_quotas,
            api_ver_services=config.cmdb.api_ver_services,
            api_ver_slas=config.cmdb.api_ver_slas,
            api_ver_user_groups=config.cmdb.api_ver_user_groups,
        )
