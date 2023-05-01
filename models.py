#user will have username, (dummy)password, boolean islogin, date last login, date created
from sqlalchemy import Boolean, Column, ForeignKey,Integer, String, Date

from db import Base
class User(Base):
    __tablename__="users"
    userid=Column(Integer, primary_key=True, index=True)
    username=Column(String)
    email=Column(String, unique=True,index=True)
    password=Column(String)
   

    avatar=Column(String, default="")
    
    is_ava_set= Column(Boolean, default=False)
    