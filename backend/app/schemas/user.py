from pydantic import BaseModel, EmailStr
from app.models.user import RoleEnum


class RegisterSchema(BaseModel):
    email:      EmailStr
    password:   str
    role:       RoleEnum
    first_name: str
    last_name:  str
    # поля студента (опционально)
    specialty:  str | None = None
    year:       int | None = None
    # поля работодателя (опционально)
    organization: str | None = None
    contact_name: str | None = None


class LoginSchema(BaseModel):
    email:    EmailStr
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type:   str = "bearer"


class UserOut(BaseModel):
    id:    int
    email: str
    role:  RoleEnum

    model_config = {"from_attributes": True}
