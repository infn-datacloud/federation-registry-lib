"""Test settings."""
from random import choice
from typing import Any, Literal, Tuple

import pytest
from pydantic import AnyHttpUrl, AnyUrl, EmailStr
from pytest_cases import parametrize, parametrize_with_cases

from app.config import Neo4jUriScheme, Settings
from tests.common.utils import random_email, random_lower_string, random_url


def random_neo4j_uri_scheme() -> Neo4jUriScheme:
    """Returns a random Neo4jUriScheme value.

    Returns:
        A random Neo4jUriScheme value.
    """
    return choice([i for i in Neo4jUriScheme])


class CaseValidSettings:
    def case_project_name(self) -> Tuple[Literal["PROJECT_NAME"], str]:
        """Returns the PROJECT_NAME and a random lowercase string.

        Returns:
            A tuple containing the key "PROJECT_NAME" and a random lowercase string.
        """
        return "PROJECT_NAME", random_lower_string()

    def case_domain(self) -> Tuple[Literal["DOMAIN"], str]:
        """Returns the DOMAIN setting and a random lowercase string.

        Returns:
            A tuple containing the key "DOMAIN" and a random lowercase string.
        """
        return "DOMAIN", random_lower_string()

    def case_api_v1(self) -> Tuple[Literal["API_V1_STR"], str]:
        """Returns the API_V1_STR setting and a random lowercase string.

        Returns:
            A tuple containing the key "API_V1_STR" and a random lowercase string.
        """
        return "API_V1_STR", f"/{random_lower_string()}"

    def case_neo4j_db_url(self) -> Tuple[Literal["NEO4J_DB_URL"], AnyHttpUrl]:
        """Returns the NEO4J_DB_URL setting and a random URL.

        Returns:
            A tuple containing the key "NEO4J_DB_URL" and a random URL.
        """
        return "NEO4J_DB_URL", random_url()

    def case_maintainer_name(self) -> Tuple[Literal["MAINTAINER_NAME"], str]:
        """Returns the MAINTAINER_NAME setting and a random Neo4jUriScheme value.

        Returns:
            A tuple containing the key "MAINTAINER_NAME" and a random Neo4jUriScheme
            value.
        """
        return "MAINTAINER_NAME", random_lower_string()

    def case_maintainer_url(self) -> Tuple[Literal["MAINTAINER_URL"], str]:
        """Returns the MAINTAINER_URL setting and a random Neo4jUriScheme value.

        Returns:
            A tuple containing the key "MAINTAINER_URL" and a random Neo4jUriScheme
            value.
        """
        return "MAINTAINER_URL", random_url()

    def case_maintainer_email(self) -> Tuple[Literal["MAINTAINER_EMAIL"], EmailStr]:
        """Returns the MAINTAINER_EMAIL setting and a random Neo4jUriScheme value.

        Returns:
            A tuple containing the key "MAINTAINER_EMAIL" and a random Neo4jUriScheme
            value.
        """
        return "MAINTAINER_EMAIL", random_email()

    def case_doc_v1_url(self) -> Tuple[Literal["DOC_V1_URL"], AnyHttpUrl]:
        """Returns the DOC_V1_URL setting and a random URL.

        Returns:
            A tuple containing the key "DOC_V1_URL" and a random URL.
        """
        return "DOC_V1_URL", random_url()


class CaseNeo4jAttr:
    def case_neo4j_server(self) -> Tuple[Literal["NEO4J_SERVER"], str]:
        """Returns the NEO4J_SERVER setting and a random lowercase string.

        Returns:
            A tuple containing the key "NEO4J_SERVER" and a random lowercase string.
        """
        return "NEO4J_SERVER", random_lower_string()

    def case_neo4j_user(self) -> Tuple[Literal["NEO4J_USER"], str]:
        """Returns the NEO4J_USER setting and a random lowercase string.

        Returns:
            A tuple containing the key "NEO4J_USER" and a random lowercase string.
        """
        return "NEO4J_USER", random_lower_string()

    def case_neo4j_password(self) -> Tuple[Literal["NEO4J_PASSWORD"], str]:
        """Returns the NEO4J_PASSWORD setting and a random lowercase string.

        Returns:
            A tuple containing the key "NEO4J_PASSWORD" and a random lowercase string.
        """
        return "NEO4J_PASSWORD", random_lower_string()

    def case_neo4j_uri_scheme(self) -> Tuple[Literal["NEO4J_URI_SCHEME"], str]:
        """Returns the NEO4J_URI_SCHEME setting and a random Neo4jUriScheme value.

        Returns:
            A tuple containing the key "NEO4J_URI_SCHEME" and a random Neo4jUriScheme
            value.
        """
        return "NEO4J_URI_SCHEME", random_neo4j_uri_scheme()


class CaseInvalidSettings:
    @parametrize(value=["", "/"])
    def case_api_v1(self, value: str) -> Tuple[Literal["API_V1_STR"], str]:
        """Returns the API_V1_STR setting and a random invalid string.

        Args:
            value (str): The value to set the API_V1_STR to.

        Returns:
            A tuple containing the key "API_V1_STR" and a random lowercase string.
        """
        return "API_V1_STR", value

    def case_neo4j_db_url_not_url(self) -> Tuple[Literal["NEO4J_DB_URL"], str]:
        return "NEO4J_DB_URL", random_lower_string()


def test_settings_default() -> None:
    """Test default value for settings."""
    settings = Settings()
    assert settings.PROJECT_NAME == Settings.__fields__.get("PROJECT_NAME").default
    assert settings.DOMAIN == Settings.__fields__.get("DOMAIN").default
    assert settings.API_V1_STR == Settings.__fields__.get("API_V1_STR").default
    assert settings.NEO4J_SERVER == Settings.__fields__.get("NEO4J_SERVER").default
    assert settings.NEO4J_USER == Settings.__fields__.get("NEO4J_USER").default
    assert settings.NEO4J_PASSWORD == Settings.__fields__.get("NEO4J_PASSWORD").default
    assert (
        settings.NEO4J_URI_SCHEME
        == Settings.__fields__.get("NEO4J_URI_SCHEME").default.value
    )

    assert settings.NEO4J_DB_URL is not None
    assert settings.NEO4J_DB_URL != ""
    assert isinstance(settings.NEO4J_DB_URL, AnyUrl)
    assert settings.NEO4J_DB_URL.scheme == settings.NEO4J_URI_SCHEME
    assert settings.NEO4J_DB_URL.user == settings.NEO4J_USER
    assert settings.NEO4J_DB_URL.password == settings.NEO4J_PASSWORD
    assert (
        f"{settings.NEO4J_DB_URL.host}:{settings.NEO4J_DB_URL.port}"
        == settings.NEO4J_SERVER
    )

    assert len(settings.ADMIN_EMAIL_LIST) == 0
    assert len(settings.TRUSTED_IDP_LIST) == 0

    assert settings.MAINTAINER_NAME is None
    assert settings.MAINTAINER_URL is None
    assert settings.MAINTAINER_EMAIL is None

    assert settings.DOC_V1_URL is not None
    assert settings.DOC_V1_URL != ""
    assert isinstance(settings.DOC_V1_URL, AnyHttpUrl)
    assert settings.DOC_V1_URL.scheme == "http"
    assert f"{settings.DOC_V1_URL.host}:{settings.DOC_V1_URL.port}" == settings.DOMAIN
    assert settings.DOC_V1_URL.path == f"{settings.API_V1_STR}/docs"


@parametrize_with_cases("key, value", cases=CaseValidSettings)
def test_settings_single_attr(key: str, value: Any) -> None:
    """Test a single attribute of the Settings class.

    Args:
        key (str): The name of the attribute to test.
        value (Any): The value to set the attribute to.

    Returns:
        None
    """
    d = {key: value}
    settings = Settings(**d)
    if isinstance(settings.__getattribute__(key), AnyUrl):
        assert str(settings.__getattribute__(key)) == value
    else:
        assert settings.__getattribute__(key) == value


@parametrize_with_cases("key, value", cases=CaseNeo4jAttr)
def test_settings_neo4j_attr(key: str, value: Any) -> None:
    """Test one of the neo4j attribute of the Settings class.

    Check that the neo4j_db_url attribute is correctly set.

    Args:
        key (str): The name of the attribute to test.
        value (Any): The value to set the attribute to.

    Returns:
        None
    """
    d = {key: value}
    settings = Settings(**d)
    if key == "NEO4J_URI_SCHEME":
        value = value.value
    assert settings.__getattribute__(key) == value

    if key == "NEO4J_SERVER":
        k = "host"
    else:
        k = key[key.rfind("_") + 1 :].lower()
    assert settings.NEO4J_DB_URL.__getattribute__(k) == value


def test_settings_neo4j_db_url_empty_str() -> None:
    settings = Settings(NEO4J_DB_URL="")
    assert settings.NEO4J_DB_URL is not None
    assert settings.NEO4J_DB_URL != ""
    assert isinstance(settings.NEO4J_DB_URL, AnyUrl)
    assert settings.NEO4J_DB_URL.scheme == settings.NEO4J_URI_SCHEME
    assert settings.NEO4J_DB_URL.user == settings.NEO4J_USER
    assert settings.NEO4J_DB_URL.password == settings.NEO4J_PASSWORD
    assert (
        f"{settings.NEO4J_DB_URL.host}:{settings.NEO4J_DB_URL.port}"
        == settings.NEO4J_SERVER
    )


def test_settings_doc_v1_url_empty_str() -> None:
    settings = Settings(DOC_V1_URL="")
    assert settings.DOC_V1_URL is not None
    assert settings.DOC_V1_URL != ""
    assert isinstance(settings.DOC_V1_URL, AnyHttpUrl)
    assert settings.DOC_V1_URL.scheme == "http"
    assert f"{settings.DOC_V1_URL.host}:{settings.DOC_V1_URL.port}" == settings.DOMAIN
    assert settings.DOC_V1_URL.path == f"{settings.API_V1_STR}/docs"


@parametrize_with_cases("key, value", cases=CaseInvalidSettings)
def test_settings_invalid_attr(key: str, value: Any) -> None:
    """Test a single attribute of the Settings class.

    Args:
        key (str): The name of the attribute to test.
        value (Any): The value to set the attribute to.

    Returns:
        None
    """
    d = {key: value}
    with pytest.raises(ValueError):
        Settings(**d)
