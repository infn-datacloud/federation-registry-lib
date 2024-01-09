"""Test settings."""
from pydantic import AnyHttpUrl, AnyUrl

from app.config import Settings, get_settings


def test_default() -> None:
    """Test default value for settings."""
    settings = get_settings()
    assert settings.PROJECT_NAME == Settings.__fields__.get("PROJECT_NAME").default
    assert settings.DOMAIN == Settings.__fields__.get("DOMAIN").default
    assert settings.API_V1_STR == Settings.__fields__.get("API_V1_STR").default
    assert settings.NEO4J_SERVER == Settings.__fields__.get("NEO4J_SERVER").default
    assert settings.NEO4J_USER == Settings.__fields__.get("NEO4J_USER").default
    assert settings.NEO4J_PASSWORD == Settings.__fields__.get("NEO4J_PASSWORD").default
    assert (
        settings.NEO4J_URI_SCHEME == Settings.__fields__.get("NEO4J_URI_SCHEME").default
    )

    assert settings.NEOMODEL_DATABASE_URL is not None
    assert settings.NEOMODEL_DATABASE_URL != ""
    assert isinstance(settings.NEOMODEL_DATABASE_URL, AnyUrl)
    assert settings.NEOMODEL_DATABASE_URL.scheme == settings.NEO4J_URI_SCHEME
    assert settings.NEOMODEL_DATABASE_URL.user == settings.NEO4J_USER
    assert settings.NEOMODEL_DATABASE_URL.password == settings.NEO4J_PASSWORD
    assert (
        f"{settings.NEOMODEL_DATABASE_URL.host}:{settings.NEOMODEL_DATABASE_URL.port}"
        == settings.NEO4J_SERVER
    )

    assert settings.DOC_V1_URL is not None
    assert settings.DOC_V1_URL != ""
    assert isinstance(settings.DOC_V1_URL, AnyHttpUrl)
    assert settings.DOC_V1_URL.scheme == "http"
    assert f"{settings.DOC_V1_URL.host}:{settings.DOC_V1_URL.port}" == settings.DOMAIN
    assert settings.DOC_V1_URL.path == f"{settings.API_V1_STR}/docs"

    assert len(settings.ADMIN_EMAIL_LIST) == 0
    assert len(settings.TRUSTED_IDP_LIST) == 0
