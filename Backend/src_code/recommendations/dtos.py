from pydantic import BaseModel


class RecommendationItem(BaseModel):
    severity: str
    message: str


class RecommendationResponse(BaseModel):
    vehicle_id: int
    recommendations: list[RecommendationItem]