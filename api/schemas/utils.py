from typing import Literal

from pydantic import BaseModel


class User(BaseModel):
    id: str
    sub: str
    given_name: str
    family_name: str
    school_id: str
    school_name: str
    role: Literal["teacher", "admin"]