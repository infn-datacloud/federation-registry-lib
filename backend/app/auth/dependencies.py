from app.config import get_settings
from fastapi import Depends
from fastapi.security import HTTPBasicCredentials, HTTPBearer
from flaat.config import AccessLevel
from flaat.fastapi import Flaat
from flaat.requirements import IsTrue
from flaat.user_infos import UserInfos

security = HTTPBearer(auto_error=False)


def check_read_access(
    client_credentials: HTTPBasicCredentials = Depends(security),
) -> bool:
    if client_credentials:
        flaat.is_authenticated()
        return True
    return False



def has_write_access(user_infos: UserInfos) -> bool:
    """Target user has write access on CMDB."""
    settings = get_settings()
    return user_infos.user_info["email"] in settings.ADMIN_EMAIL_LIST


flaat = Flaat()
flaat.set_access_levels(
    [
        AccessLevel("write", IsTrue(has_write_access)),
    ]
)
flaat.set_trusted_OP_list(get_settings().TRUSTED_IDP_LIST)
flaat.set_request_timeout(30)
