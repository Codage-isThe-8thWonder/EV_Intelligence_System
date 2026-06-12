from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from src_code.utils.db import get_db
from src_code.forecasting import controller


from src_code.forecasting.dtos import ForecastResponse

forecast_routes = APIRouter(prefix="/forecasting")

@forecast_routes.get("/{vehicle_id}", response_model=ForecastResponse)
def get_forecast(vehicle_id: int, db: Session = Depends(get_db)):
    return controller.get_forecast(vehicle_id, db)