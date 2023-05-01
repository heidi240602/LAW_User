from fastapi import Depends, HTTPException, FastAPI
from sqlalchemy.orm import Session
import models, schemas,crud
from db import SessionLocal, engine
from encrypt import check_pass, hash_pass
from auth.jwt_handler import signJWT
from auth.jwt_bearer import JWTBearer

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Dependency
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close

@app.post("/users/")
def create_user(user:schemas.UserCreate, db:Session=Depends(get_db)):
    db_user = crud.get_user_by_email(db,email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    crud.create_user(db=db, user=user)
    return signJWT(user.email)

@app.post("/users/login")
def user_login(user: schemas.UserLogin, db:Session=Depends(get_db)):
    if crud.check_user(db, user):
        return signJWT(user.email)
    raise HTTPException(status_code=401, detail="Wrong login details!")

# kunci
@app.get("/users/{usermail}", dependencies=[Depends(JWTBearer())],  response_model=schemas.User)
def get_user_by_email(usermail:str, db: Session=Depends(get_db)):
    db_user=crud.get_user_by_email(db, email=usermail)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# kunci atau usulin mending dihapus
@app.get("/users/pwd/{usermail}", dependencies=[Depends(JWTBearer())], response_model=schemas.UserPass)
def get_user_pass(usermail:str, db: Session=Depends(get_db)):
    db_user=crud.get_user_by_email(db, email=usermail)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# kunci
@app.put("/users/picture/{usermail}", dependencies=[Depends(JWTBearer())], response_model=schemas.User)
def change_user_pict(user:schemas.UserPict ,usermail:str, db:Session=Depends(get_db)):
    db_user=crud.get_user_by_email(db, email=usermail)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.avatar=user.pfp
    db_user.is_ava_set=True
    db.add(db_user)
    db.commit()
    return db_user

# kunci
@app.put("/users/pwd/{usermail}", dependencies=[Depends(JWTBearer())], response_model=schemas.User)
def change_pwd(user:schemas.UserPwd ,usermail:str, db:Session=Depends(get_db)):
    db_user=crud.get_user_by_email(db, email=usermail)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    #result=user.old_pass==db_user.password
    result=check_pass(user_pwd=user.old_pass,pwd=db_user.password)
    if result==False:
        raise HTTPException(status_code=404, detail="Wrong old password")
    db_user.password=hash_pass(user.new_pass)
    db.add(db_user)
    db.commit()
    return db_user


