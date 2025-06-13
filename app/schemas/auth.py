from pydantic import BaseModel, Field


class UserRegistrationInput(BaseModel):
    name: str = Field(min_length=8, max_length=64)
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=3, max_length=64)

class UserLoginInput(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=3, max_length=64)

class UserLoginOutput(BaseModel):
    id: int
    name: str
    username: str
    jwt_token: str


