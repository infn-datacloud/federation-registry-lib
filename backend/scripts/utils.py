import os
from typing import Dict, List, Optional, Tuple

import yaml
from logger import logger
from models.cmdb.quota import BlockStorageQuotaWrite, ComputeQuotaWrite
from models.config import (
    AuthMethod,
    ChosenIDP,
    ConfigIn,
    ConfigOut,
    Project,
    TrustedIDPOut,
    URLs,
)
from pydantic import UUID4


def choose_idp(
    *, project_sla: UUID4, idp_list: List[TrustedIDPOut]
) -> Optional[ChosenIDP]:
    for trusted_idp in idp_list:
        for user_group in trusted_idp.user_groups:
            if project_sla in [sla.doc_uuid for sla in user_group.slas]:
                return ChosenIDP(
                    token=trusted_idp.token,
                    name=trusted_idp.relationship.idp_name,
                    protocol=trusted_idp.relationship.protocol,
                    issuer=trusted_idp.endpoint,
                )
    logger.error(
        "Configuration error: Project's SLA document ID "
        f"{project_sla} does not match any of the SLAs "
        "in the Trusted Identity Provider list."
    )
    return None


def get_identity_providers(
    *, provider_idps: List[AuthMethod], trusted_idps: List[TrustedIDPOut]
) -> List[TrustedIDPOut]:
    logger.info("Retrieve and merge identity providers data.")
    logger.info("Include also user groups and related SLAs.")
    identity_providers = []
    for idp in provider_idps:
        for trusted_idp in trusted_idps:
            if idp.endpoint == trusted_idp.endpoint:
                trusted_idp.relationship = idp
                identity_providers.append(trusted_idp)
    return identity_providers


def load_config(*, base_path: str = ".", fname: str = ".config.yaml") -> ConfigOut:
    logger.info("Loading configuration")
    with open(os.path.join(base_path, fname)) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    conf = ConfigIn(**config)

    d = {}
    for k, v in conf.cmdb.api_ver.dict().items():
        d[k] = os.path.join(conf.cmdb.base_url, "api", f"{v}", f"{k}")
    urls = URLs(**d)
    idps = []
    for idp in conf.trusted_idps:
        idps.append(TrustedIDPOut(**idp.dict(), endpoint=idp.issuer))
    conf = ConfigOut(
        cmdb_urls=urls,
        trusted_idps=idps,
        openstack=conf.openstack,
        kubernetes=conf.kubernetes,
    )
    logger.info("Configuration loaded")
    return conf


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
