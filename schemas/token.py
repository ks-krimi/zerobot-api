from typing import Union

from pydantic import BaseModel


# schema for access token
class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class TokenData(BaseModel):
    id: Union[str, None] = None
