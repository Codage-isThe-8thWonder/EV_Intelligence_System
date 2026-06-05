from sqlalchemy import Column,Integer,String,ForeignKey
from src_code.utils.db import Base

class VehicleModel(Base):
    __tablename__ = "vehicles"

    user_id = Column(Integer,ForeignKey("users.user_id" ,ondelete="CASCADE"), nullable=True)
    vehicle_id = Column(Integer,primary_key=True)
    manufacturer = Column(String)
    model = Column(String)