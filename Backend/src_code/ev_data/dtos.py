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