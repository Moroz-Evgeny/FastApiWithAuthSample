from datetime import datetime
import re, uuid
from typing import Optional

from fastapi import File, Form, HTTPException, UploadFile

from pydantic import BaseModel
from pydantic import constr
from pydantic import EmailStr
from pydantic import field_validator


LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:
        from_attributes = True
        exclude_none = True


class ShowUser(TunedModel):
    user_id: uuid.UUID | None = None
    login: str
    role: str 
    is_active: bool | None = None

class UpdateUserRequest(BaseModel):
    login: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    
class UserCreate(BaseModel):
    login: str
    first_name: str
    middle_name: str
    last_name: str
    password: str


    @field_validator("first_name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(status_code=422, detail="Name incorrect")
        return value
    
    @field_validator("middle_name")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(status_code=422, detail="Surname incorrect")
        return value
    
    @field_validator("last_name")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(status_code=422, detail="Lastname incorrect")
        return value

class Token(BaseModel):
    access_token: str
    token_type: str 
