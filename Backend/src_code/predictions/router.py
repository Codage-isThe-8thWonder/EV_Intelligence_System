from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src_code.predictions.dtos import PredictionResponseDTO
from src_code.predictions import controller
from src_code.utils.db import get_db
from src_code.users.models import UserModel
from src_code.users.controller import is_authenticated


prediction_routes = APIRouter(prefix="/predictions")


@prediction_routes.get("/{vehicle_id}",response_model=PredictionResponseDTO)
def get_predictions(vehicle_id: int, db: Session = Depends(get_db), user:UserModel = Depends(is_authenticated)):
    return controller.get_predictions(vehicle_id,db, user)