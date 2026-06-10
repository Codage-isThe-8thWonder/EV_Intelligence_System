from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from src_code.utils.db import Base

class EVDataModel(Base):

    __tablename__ = "ev_data"

    data_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    vehicle_id = Column(
        Integer,
        ForeignKey("vehicles.vehicle_id"),
        nullable=False
    )

    timestamp = Column(
        DateTime,
        nullable=False
    )

    soc = Column(Float, nullable=True)
    soh = Column(Float, nullable=True)

    battery_voltage = Column(Float, nullable=True)
    battery_current = Column(Float, nullable=True)
    battery_temperature = Column(Float, nullable=True)

    charge_cycles = Column(Integer, nullable=True)

    motor_temperature = Column(Float, nullable=True)
    motor_vibration = Column(Float, nullable=True)

    power_consumption = Column(Float, nullable=True)

    ambient_temperature = Column(Float, nullable=True)

    load_weight = Column(Float, nullable=True)

    driving_speed = Column(Float, nullable=True)

    distance_traveled = Column(Float, nullable=True)

    motor_torque = Column(Float, nullable=True)

    motor_rpm = Column(Float, nullable=True)

    brake_pad_wear = Column(Float, nullable=True)

    brake_pressure = Column(Float, nullable=True)

    reg_brake_efficiency = Column(Float, nullable=True)

    tire_pressure = Column(Float, nullable=True)

    tire_temperature = Column(Float, nullable=True)

    suspension_load = Column(Float, nullable=True)

    ambient_humidity = Column(Float, nullable=True)

    idle_time = Column(Float, nullable=True)

    route_roughness = Column(Float, nullable=True)

    maintenance_type = Column(Integer, nullable=True)