from pydantic import BaseModel


class ForecastValues(BaseModel):

    one_hour: float

    six_hours: float

    twenty_four_hours: float


class ForecastResponse(BaseModel):

    vehicle_id: int

    soc_forecast: ForecastValues

    voltage_forecast: ForecastValues