from pydantic import BaseModel


class LoginSuccess(BaseModel):
    success: bool = True
