

from pydantic import BaseModel


class PredictionResponseDTO(BaseModel):

    rul: float

    failure_probability: float

    component_health_score: float

    estimated_driving_range: float

    estimated_charging_time: float