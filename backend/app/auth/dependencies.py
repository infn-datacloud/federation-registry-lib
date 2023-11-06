from app.config import get_settings
from fastapi import Depends
from fastapi.security import HTTPBasicCredentials, HTTPBearer
from flaat.config import AccessLevel
from flaat.fastapi import Flaat
from flaat.requirements import IsTrue
from flaat.user_infos import UserInfos

strict_security = HTTPBearer()
lazy_security = HTTPBearer(auto_error=False)


def has_write_access(user_infos: UserInfos) -> bool:
    """Target user has write access on CMDB."""
    settings = get_settings()
    return user_infos.user_info.get("email") in settings.ADMIN_EMAIL_LIST


flaat = Flaat()
flaat.set_access_levels([AccessLevel("write", IsTrue(has_write_access))])
flaat.set_trusted_OP_list(get_settings().TRUSTED_IDP_LIST)
flaat.set_request_timeout(30)


def check_read_access(
    client_credentials: HTTPBasicCredentials = Depends(lazy_security),
) -> bool:
    """Return True if the request contains a valid token."""
    if client_credentials:
        flaat.is_authenticated()
        return True
    return False


def check_write_access(
    client_credentials: HTTPBasicCredentials = Depends(strict_security),
) -> bool:
    """At first, validate user authentication, then, check user write access rights."""
    flaat.access_level("write")
