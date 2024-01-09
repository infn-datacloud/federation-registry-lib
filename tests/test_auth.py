"""Test custom  authentication functions."""
import pytest
from flaat.user_infos import UserInfos

from app.auth import has_write_access
from app.main import settings

MOCK_READ_EMAIL = "user@test.it"
MOCK_WRITE_EMAIL = "admin@test.it"


@pytest.fixture
def user_infos_with_write_email() -> UserInfos:
    """Fake user with email. It has write access rights."""
    return UserInfos(
        access_token_info=None,
        user_info={"email": MOCK_WRITE_EMAIL},
        introspection_info=None,
    )


@pytest.fixture
def user_infos_with_read_email() -> UserInfos:
    """Fake user with email. It has only read access rights."""
    return UserInfos(
        access_token_info=None,
        user_info={"email": MOCK_READ_EMAIL},
        introspection_info=None,
    )


@pytest.fixture
def user_infos_without_email() -> UserInfos:
    """Fake user without email."""
    return UserInfos(access_token_info=None, user_info={}, introspection_info=None)


def test_check_write_access(user_infos_with_write_email: UserInfos) -> None:
    """Test user has write access rights."""
    settings.ADMIN_EMAIL_LIST = [MOCK_WRITE_EMAIL]
    assert has_write_access(user_infos_with_write_email)


def test_check_not_write_access(
    user_infos_with_read_email: UserInfos, user_infos_without_email: UserInfos
) -> None:
    """Test user has no write access rights."""
    settings.ADMIN_EMAIL_LIST = [MOCK_WRITE_EMAIL]
    assert not has_write_access(user_infos_with_read_email)
    assert not has_write_access(user_infos_without_email)
