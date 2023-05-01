import bcrypt
from sqlalchemy.orm import Session
import models, schemas
from datetime import datetime
import random
import string
from encrypt import hash_pass

def make_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(8))
    return password

def get_user(db:Session, user_id:int):
    return db.query(models.User).filter(models.User.id==user_id).first()

def get_user_by_email(db:Session, email:str):
    return db.query(models.User).filter(models.User.email==email).first()

def create_user(db: Session, user:schemas.UserCreate):
    hash_pwd=hash_pass(user.password)
    db_user=models.User(email=user.email, username=user.username, password=hash_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def check_user(db:Session, user:schemas.UserLogin):
    db_user = db.query(models.User).filter(models.User.email==user.email).first()
    if bcrypt.checkpw(user.password.encode('utf-8'), db_user.password.encode('utf-8')):
        return True
    return False