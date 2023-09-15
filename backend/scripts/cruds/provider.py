from typing import Dict

from cruds.core import BasicCRUD
from models.cmdb import ProviderQuery, ProviderRead, ProviderWrite
from pydantic import AnyHttpUrl


class ProviderCRUD(BasicCRUD[ProviderWrite, ProviderRead, ProviderQuery]):
    def __init__(
        self,
        get_url: AnyHttpUrl,
        post_url: AnyHttpUrl,
        patch_url: AnyHttpUrl,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            type="Provider",
            read_schema=ProviderRead,
            write_schema=ProviderWrite,
            get_url=get_url,
            post_url=post_url,
            patch_url=patch_url,
            read_headers=read_headers,
            write_headers=write_headers,
        )
