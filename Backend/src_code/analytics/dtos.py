
from pydantic import BaseModel
from datetime import datetime


class SummaryCardResponse(BaseModel):

    avg_soc: float | None

    avg_soh: float | None

    max_battery_temperature: float | None

    avg_driving_speed: float | None

    total_distance: float | None

    avg_power_consumption : float | None




class TrendPoint(BaseModel):

    timestamp: datetime

    value: float | None


class OperationalTrendsResponse(BaseModel):

    soc: list[TrendPoint]

    battery_temperature: list[TrendPoint]

    driving_speed: list[TrendPoint]

    power_consumption: list[TrendPoint]

    motor_temperature: list[TrendPoint]



class BatteryAnalyticsResponse(BaseModel):

    soh: list[TrendPoint]

    battery_voltage: list[TrendPoint]

    battery_current: list[TrendPoint]

    charge_cycles: list[TrendPoint]



class SpeedPowerPoint(BaseModel):

    driving_speed: float | None

    power_consumption: float | None


class TemperaturePoint(BaseModel):

    ambient_temperature: float | None

    battery_temperature: float | None


class VehiclePerformanceResponse(BaseModel):

    distance_traveled: list[TrendPoint]

    speed_vs_power: list[SpeedPowerPoint]

    ambient_vs_battery_temperature: list[TemperaturePoint]