from sqlalchemy import Column, Integer, String
from src_code.utils.db import Base


class UserModel(Base):
    __tablename__ = "users"

    user_id = Column(Integer,primary_key=True,autoincrement=True)
    mobile_number = Column(String)
    username = Column(String,nullable=False)
    email = Column(String,unique=True,nullable=False)
    hash_password = Column(String,nullable=False)