from datetime import datetime
from pydantic import BaseModel


class EVDataSchema(BaseModel):

    vehicle_id: int

    timestamp: datetime

    soc: float | None = None
    soh: float | None = None

    battery_voltage: float | None = None
    battery_current: float | None = None
    battery_temperature: float | None = None

    charge_cycles: int | None = None

    motor_temperature: float | None = None
    motor_vibration: float | None = None

    power_consumption: float | None = None

    ambient_temperature: float | None = None

    load_weight: float | None = None

    driving_speed: float | None = None
    distance_traveled: float | None = None

    motor_torque: float | None = None
    motor_rpm: float | None = None

    brake_pad_wear: float | None = None
    brake_pressure: float | None = None
    reg_brake_efficiency: float | None = None

    tire_pressure: float | None = None
    tire_temperature: float | None = None

    suspension_load: float | None = None

    ambient_humidity: float | None = None

    idle_time: float | None = None

    route_roughness: float | None = None
    maintenance_type: int | None = None



class EVDataResponseSchema(BaseModel):

    data_id: int

    vehicle_id: int

    timestamp: datetime

    soc: float | None = None
    soh: float | None = None

    battery_voltage: float | None = None
    battery_current: float | None = None
    battery_temperature: float | None = None

    charge_cycles: int | None = None

    motor_temperature: float | None = None
    motor_vibration: float | None = None

    power_consumption: float | None = None

    ambient_temperature: float | None = None

    load_weight: float | None = None

    driving_speed: float | None = None
    distance_traveled: float | None = None

    motor_torque: float | None = None
    motor_rpm: float | None = None

    brake_pad_wear: float | None = None
    brake_pressure: float | None = None
    reg_brake_efficiency: float | None = None

    tire_pressure: float | None = None
    tire_temperature: float | None = None

    suspension_load: float | None = None

    ambient_humidity: float | None = None

    idle_time: float | None = None

    route_roughness: float | None = None
    maintenance_type: int | None = None
