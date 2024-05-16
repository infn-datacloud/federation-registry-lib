"""Test custom  authentication functions."""
from flaat.user_infos import UserInfos

from fed_reg.auth import has_write_access
from fed_reg.main import settings
from tests.utils import MOCK_WRITE_EMAIL


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
