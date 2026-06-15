
from sqlalchemy import Column, Integer, String, ForeignKey
from src_code.utils.db import Base


class AppSettingsModel(Base):
    __tablename__ = "app_settings"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        unique=True,
        nullable=False
    )

    theme = Column(String, default="system")

    distance_unit = Column(String, default="km")

    temperature_unit = Column(String, default="celsius")

    default_vehicle_id = Column(
        Integer,
        ForeignKey("vehicles.vehicle_id"),
        nullable=True
    )