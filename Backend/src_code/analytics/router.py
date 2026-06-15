from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src_code.utils.db import get_db
from src_code.analytics.dtos import SummaryCardResponse, OperationalTrendsResponse, VehiclePerformanceResponse, BatteryAnalyticsResponse
from src_code.analytics import controller
from src_code.users.controller import is_authenticated
from src_code.users.models import UserModel


analytics_routes = APIRouter(prefix="/analytics")


@analytics_routes.get("/summary_card/{vehicle_id}", response_model=SummaryCardResponse)
def get_vehicle_summary(vehicle_id: int, db: Session = Depends(get_db), user:UserModel = Depends(is_authenticated)):
    return controller.get_summary_card(
        vehicle_id,
        db,
        user
    )


@analytics_routes.get("/trends/{vehicle_id}", response_model=OperationalTrendsResponse)
def get_operational_trends(vehicle_id: int, db: Session = Depends(get_db), user:UserModel = Depends(is_authenticated)):
    return controller.get_operational_trends(
        vehicle_id,
        db,
        user
    )


@analytics_routes.get("/battery-analytics/{vehicle_id}",response_model=BatteryAnalyticsResponse)
def get_battery_analytics(vehicle_id: int,db: Session = Depends(get_db), user:UserModel = Depends(is_authenticated)):
    return controller.get_battery_analytics(
        vehicle_id,
        db,
        user
    )



@analytics_routes.get("/vehicle-performance/{vehicle_id}",response_model=VehiclePerformanceResponse)
def get_vehicle_performance(vehicle_id: int,db: Session = Depends(get_db), user:UserModel = Depends(is_authenticated)):
    return controller.get_vehicle_performance(
        vehicle_id,
        db,
        user
    )