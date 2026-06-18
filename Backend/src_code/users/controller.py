from fastapi import HTTPException, Request, Depends
from sqlalchemy import or_ 
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from src_code.users.dtos import UserSchema, LoginSchema
from src_code.users.models import UserModel
from src_code.utils.settings import settings
from src_code.utils.db import get_db
from pwdlib import PasswordHash
from jwt.exceptions import InvalidTokenError
import jwt



password_hash = PasswordHash.recommended()
def get_password_hash(password):
    return password_hash.hash(password)


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password,hashed_password)


def register(body:UserSchema,db:Session):

    is_user = db.query(UserModel).filter(UserModel.username==body.username).first()
    if is_user:
        raise HTTPException(400, detail="Username already exist")
    
    is_user = db.query(UserModel).filter(UserModel.email == body.email).first()
    if is_user:
        raise HTTPException(400, detail="Email address already Registered")
    
    is_user = db.query(UserModel).filter(UserModel.mobile_number==body.mobile_number).first()
    if is_user:
        raise HTTPException(400, detail="Mobile Number already Registered")
    
    hash_password = get_password_hash(body.password)

    new_user = UserModel(
        mobile_number = body.mobile_number,
        username = body.username,
        hash_password = hash_password,
        email = body.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user




def login_user(body:LoginSchema, db:Session):
    user = db.query(UserModel).filter(or_(
        UserModel.email == body.identifier,
        UserModel.mobile_number == body.identifier)).first()
    
    if not user:
        raise HTTPException(status_code= 401, detail = "Email Id not registered")
    
    
    if not verify_password(body.password,user.hash_password):
        raise HTTPException(status_code= 401, detail = "You entered wrong password")
    

    exp_time = datetime.now() + timedelta(minutes = settings.EXP_TIME)
    token = jwt.encode({"id":user.user_id, "exp":exp_time.timestamp()}, settings.SECRET_KEY, settings.ALGORITHM)
    return {
        "token" : token
    }




def is_authenticated(request:Request, db:Session= Depends(get_db)):
    
    try:
        token = request.headers.get("Authorization")

        if not token:
            raise HTTPException(status_code=401, detail="unauthorized user")
        
        token = token.split(" ")[-1]
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        curr_id = data.get("id")

        
        user = db.query(UserModel).filter(UserModel.user_id==curr_id).first()
        if not user:
            raise HTTPException(status_code= 401, detail = "Unauthorized user")
        return user
    
    except InvalidTokenError:
        raise HTTPException(status_code= 401, detail = "Unauthorized user")
