from app.provider.schemas_extended import UserGroupCreateExtended, UserGroupReadExtended
from app.user_group.schemas import UserGroupQuery


class UserGroupWrite(UserGroupCreateExtended):
    ...


class UserGroupRead(UserGroupReadExtended):
    ...


class UserGroupQuery(UserGroupQuery):
    ...
