import requests
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from ssl import SSLError

from app.auth.schemas import TokenData
from app.config import Settings, get_settings

settings = get_settings()

oidc_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.IDP_CONF.get("authorization_endpoint"),
    tokenUrl=settings.IDP_CONF.get("token_endpoint"),
)


async def get_current_user(
    settings: Settings = Depends(get_settings),
    token: str = Depends(oidc_scheme),
) -> TokenData:
    try:
        resp = requests.get(
            settings.IDP_CONF.get("userinfo_endpoint"),
            params={"access_token": token},
            verify=settings.CA,
        )
    except SSLError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Certificate validation failed",
        )
    return resp.json()
