from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None
    # To-do: Add scopes: scopes: List[str] = []
    # -> see OAuth2 scopes in FastAPI tutorial