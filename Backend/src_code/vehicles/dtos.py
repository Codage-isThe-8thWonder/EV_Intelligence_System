from pydantic import BaseModel

class VehicleSchema(BaseModel):
    manufacturer:str
    model:str


class VehicleResponseSchema(BaseModel):
    vehicle_id:int
    manufacturer:str
    model:str

