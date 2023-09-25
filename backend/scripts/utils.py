import os
from typing import Dict, List, Optional, Tuple

import yaml
from logger import logger
from models.cmdb.identity_provider import IdentityProviderWrite
from models.cmdb.quota import BlockStorageQuotaWrite, ComputeQuotaWrite
from models.config import AuthMethod, ConfigIn, ConfigOut, Project, TrustedIDPOut, URLs
from pydantic import AnyHttpUrl


def choose_idp(
    *, identity_providers: List[AuthMethod], preferred_idp_list: List[AnyHttpUrl]
) -> AuthMethod:
    for idp_url in preferred_idp_list:
        for chosen_idp in identity_providers:
            if idp_url == chosen_idp.endpoint:
                logger.info(f"Chosen identity provider: {chosen_idp.endpoint}")
                return chosen_idp


def get_identity_providers(
    idp_list: List[AuthMethod],
) -> List[IdentityProviderWrite]:
    logger.info("Retrieve provider authorized identity providers")
    identity_providers = []
    for idp in idp_list:
        identity_providers.append(
            IdentityProviderWrite(
                endpoint=idp.endpoint,
                group_claim=idp.group_claim,
                relationship={"idp_name": idp.name, "protocol": idp.protocol},
            )
        )
    return identity_providers


def load_config(*, base_path: str = ".", fname: str = ".config.yaml") -> ConfigOut:
    logger.info("Loading configuration")
    with open(os.path.join(base_path, fname)) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    logger.info("Configuration loaded")
    conf = ConfigIn(**config)

    d = {}
    for k, v in conf.cmdb.api_ver.dict().items():
        d[k] = os.path.join(conf.cmdb.base_url, "api", f"{v}", f"{k}")
    urls = URLs(**d)

    idps = []
    for idp in conf.trusted_idps:
        idps.append(TrustedIDPOut(**idp.dict(), endpoint=idp.issuer))

    return ConfigOut(
        cmdb_urls=urls,
        trusted_idps=idps,
        openstack=conf.openstack,
        kubernetes=conf.kubernetes,
    )


def get_read_write_headers(*, token: str) -> Tuple[Dict[str, str], Dict[str, str]]:
    read_header = {"authorization": f"Bearer {token}"}
    write_header = {
        **read_header,
        "accept": "application/json",
        "content-type": "application/json",
    }
    return (read_header, write_header)


def get_per_user_compute_quotas(
    *, project: Project, curr_region: str
) -> Optional[ComputeQuotaWrite]:
    if len(project.per_region_props) > 0:
        region_props = next(
            filter(lambda x: x.region_name == curr_region, project.per_region_props),
            None,
        )
        if region_props is not None:
            if region_props.per_user_limits is not None:
                if region_props.per_user_limits.compute is not None:
                    return ComputeQuotaWrite(
                        **region_props.per_user_limits.compute.dict(exclude_none=True),
                        project=project.id,
                    )
    if project.per_user_limits is not None:
        if project.per_user_limits.compute is not None:
            return ComputeQuotaWrite(
                **project.per_user_limits.compute.dict(exclude_none=True),
                project=project.id,
            )
    return None


def get_per_user_block_storage_quotas(
    *, project: Project, curr_region: str
) -> Optional[BlockStorageQuotaWrite]:
    if len(project.per_region_props) > 0:
        region_props = next(
            filter(lambda x: x.region_name == curr_region, project.per_region_props),
            None,
        )
        if region_props is not None:
            if region_props.per_user_limits is not None:
                if region_props.per_user_limits.block_storage is not None:
                    return BlockStorageQuotaWrite(
                        **region_props.per_user_limits.block_storage.dict(
                            exclude_none=True
                        ),
                        project=project.id,
                    )
    if project.per_user_limits is not None:
        if project.per_user_limits.block_storage is not None:
            return BlockStorageQuotaWrite(
                **project.per_user_limits.block_storage.dict(exclude_none=True),
                project=project.id,
            )
    return None
