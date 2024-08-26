from pydantic import BaseModel, validator
from fastapi.exceptions import RequestValidationError

class AccountBase(BaseModel):
    username: str
    password: str
        

class AccountCreation(AccountBase):
    class Config:
        # orm_mode = True
        from_attributes = True

    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise RequestValidationError("Username too short, minimum 3 characters")
        if len(v) > 32:
            raise RequestValidationError("Username too long, maximum 32 characters")
        return v

    @validator('password')
    def validate_password(cls, v):
        errors = []
        if len(v) < 8:
            errors.append("Password too short, minimum 8 characters")
        if len(v) > 32:
            errors.append("Password too long, maximum 32 characters")
        has_upper, has_lower, has_num = False, False, False
        for c in v:
            if not has_upper and c.isupper():
                has_upper = True
            if not has_lower and c.islower():
                has_lower = True
            if not has_num and c.isnumeric():
                has_num = True
        if not has_upper:
            errors.append("Password requires at least one uppercase letter")
        if not has_lower:
            errors.append("Password requires at least one lower case letter")
        if not has_num:
            errors.append("Password requires at least one numeric digit")
        if errors:
            raise RequestValidationError('; '.join(errors))
        return v


class AccountValidation(AccountBase):
    class Config:
        # orm_mode = True
        from_attributes = True


class Response(BaseModel):
    success: bool
    reason: str
