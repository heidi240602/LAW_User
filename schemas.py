from pydantic import BaseModel
import datetime

class UserBase(BaseModel):
    email:str

class UserCreate(UserBase):
    username:str
    password:str

class UserPict(BaseModel):
    pfp:str

class UserPwd(BaseModel):
    old_pass:str
    new_pass:str


class User(UserBase):
    userid: int
    username:str
    is_ava_set: bool
    avatar:str
    
    class Config:
        orm_mode = True


class UserPass(UserBase):
    password:str
    class Config:
        orm_mode = True

class UserLogin(UserBase):
    password : str