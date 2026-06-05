from fastapi import APIRouter ,Depends, status, Request
from src_code.users.dtos import UserResponseSchema, UserSchema, LoginSchema
from sqlalchemy.orm import Session
from src_code.utils.db import get_db
from src_code.users import controller

user_routes = APIRouter(prefix="/users")

@user_routes.post("/register" , response_model=UserResponseSchema , status_code=status.HTTP_201_CREATED)
def user_register(body:UserSchema , db:Session = Depends(get_db)):
    return controller.register(body,db)


@user_routes.post("/login", status_code=status.HTTP_200_OK )
def login(body:LoginSchema,db:Session = Depends(get_db)):
    return controller.login_user(body,db)


@user_routes.get("/is_auth", response_model=UserResponseSchema , status_code=status.HTTP_200_OK)
def is_auth(request:Request, db:Session = Depends(get_db)):
    return controller.is_authenticated(request, db)