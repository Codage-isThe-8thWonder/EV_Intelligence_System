from pydantic import BaseModel

class UserSchema(BaseModel):
    mobile_number : str
    username : str
    password : str
    email : str


class UserResponseSchema(BaseModel):
    user_id : int
    username : str
    email : str
    mobile_number : str


class LoginSchema(BaseModel):
    identifier : str
    password : str