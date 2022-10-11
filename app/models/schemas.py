from datetime import datetime
from typing import Optional,List
from unicodedata import category
from pydantic import BaseModel, EmailStr,constr,Field
from enum import Enum


class Gender(str,Enum):
    MALE = "Male"
    FEMALE = "Female"

class UserCreate(BaseModel):

    first_name: str = Field(min_length=1, max_length=250)
    username: constr(regex="^[A-Za-z0-9-_]+$", to_lower=True, strip_whitespace=True)
    last_name: str = Field(min_length=1, max_length=250)
    gender: Gender 
    email: EmailStr
    password: str

class UserOutput(BaseModel):
    id : int
    username:str
    email : EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr 
    password: str

class Reservations(BaseModel):
    name : str
    booking_time : datetime
    Room_number: int
    

class Reservations_Output(BaseModel):
    id : int
    name : str
    booking_time : datetime
    Room_number: int
    owner_id: int
    owner: UserOutput
    class Config:
        orm_mode = True

 
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id : Optional[str] = None

class Email(BaseModel):
    email: EmailStr

class Password(BaseModel):
    password: str