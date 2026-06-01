from sqlalchemy import Column,Integer,String
from src_code.utils.db import Base

class VehicleModel(Base):
    __tablename__ = "vehicles"

    vehicle_id = Column(Integer,primary_key=True)
    manufacturer = Column(String)
    model = Column(String)