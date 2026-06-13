
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src_code.utils.db import get_db
from src_code.recommendations import controller
from src_code.recommendations.dtos import RecommendationResponse


recommendations_routes = APIRouter(prefix="/recommendations")

@recommendations_routes.get("/{vehicle_id}", response_model=RecommendationResponse)
def recommendations(vehicle_id: int, db: Session = Depends(get_db)):
    return controller.get_recommendations(vehicle_id,db)