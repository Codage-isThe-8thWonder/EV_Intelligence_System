from sqlalchemy import Column, Integer, String, ForeignKey, Float
from src_code.utils.db import Base

class VehicleModel(Base):
    __tablename__ = "vehicles"

    user_id = Column(Integer,ForeignKey("users.user_id" ,ondelete="CASCADE"), nullable=False)
    vehicle_id = Column(Integer,primary_key=True)
    nickname = Column(String)
    manufacturer = Column(String)
    model = Column(String)
    battery_capacity = Column(Float ,nullable=True)