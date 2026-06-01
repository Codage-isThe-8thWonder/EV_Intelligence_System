from fastapi import APIRouter, Depends , status
from sqlalchemy.orm import Session
from src_code.utils.db import get_db
from src_code.vehicles.dtos import VehicleSchema, VehicleResponseSchema
from src_code.vehicles import controller

vehicle_routes = APIRouter(prefix="/vehicles")

@vehicle_routes.post("/add", response_model=VehicleResponseSchema, status_code=status.HTTP_201_CREATED)
def add_vehicle(body:VehicleSchema,db:Session=Depends(get_db)):
    return controller.add_vehicle(body,db)