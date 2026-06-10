from pydantic import BaseModel

class VehicleSchema(BaseModel):
    manufacturer:str
    model:str
    nickname: str | None = None
    battery_capacity: float | None = None


class VehicleResponseSchema(BaseModel):
    vehicle_id:int
    manufacturer:str
    model:str
    nickname: str | None = None
    battery_capacity: float | None = None

