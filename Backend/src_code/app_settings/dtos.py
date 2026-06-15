from typing import Optional
from pydantic import BaseModel


class UpdateAppSettingsRequest(BaseModel):

    theme: Optional[str] = None
    distance_unit: Optional[str] = None
    temperature_unit: Optional[str] = None
    default_vehicle_id: Optional[int] = None


class AppSettingsResponse(BaseModel):

    id: int
    user_id: int

    theme: str

    distance_unit: str
    temperature_unit: str

    default_vehicle_id: Optional[int]