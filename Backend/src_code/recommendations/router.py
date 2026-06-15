
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src_code.utils.db import get_db
from src_code.recommendations import controller
from src_code.recommendations.dtos import RecommendationResponse
from src_code.users.models import UserModel
from src_code.users.controller import is_authenticated


recommendations_routes = APIRouter(prefix="/recommendations")

@recommendations_routes.get("/{vehicle_id}", response_model=RecommendationResponse)
def recommendations(vehicle_id: int, db: Session = Depends(get_db),user:UserModel = Depends(is_authenticated)):
    return controller.get_recommendations(vehicle_id,db,user)