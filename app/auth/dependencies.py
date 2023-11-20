from functools import wraps
from typing import Any, Callable

from fastapi import HTTPException, status
from fastapi.security import HTTPBasicCredentials, HTTPBearer
from flaat.config import AccessLevel
from flaat.fastapi import Flaat
from flaat.requirements import IsTrue
from flaat.user_infos import UserInfos

from app.config import get_settings

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


def check_read_access(view_func: Callable) -> Callable[..., Any]:
    """Check read access for the given function and return a wrapper.

    If the client_credentials object has a token, check it is a valid one using the
    flaat is_authenticated function. On failure execute the received function setting
    the authentication to False.
    If the client_credentials object is None, return the function setting the
    authentication to False."""

    @wraps(view_func)
    def wrapper(
        auth: bool,
        client_credentials: HTTPBasicCredentials,
        *args,
        **kwargs,
    ):
        if client_credentials:
            return flaat.is_authenticated(
                on_failure=view_func(*args, **kwargs, auth=False)
            )(view_func(*args, **kwargs, auth=True))
        return view_func(*args, **kwargs, auth=False)

    return wrapper.__wrapped__


def check_write_access(view_func: Callable) -> Callable[..., Any]:
    """Check write access for the given function and return a wrapper.

    Verify that client_credentials object has a valid token with write access."""

    @wraps(view_func)
    def wrapper(
        client_credentials: HTTPBasicCredentials,
        *args,
        **kwargs,
    ):
        return flaat.access_level(
            "write",
            on_failure=HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                msg="Not authenticated",
            ),
        )(view_func(*args, **kwargs))

    return wrapper
