from typing import List
from pydantic import UUID4, BaseModel, EmailStr


class TokenData(BaseModel):
    sub: UUID4
    username: str
    given_name: str
    family_name: str
    email: EmailStr
    groups: List[str]
