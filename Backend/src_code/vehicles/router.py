from fastapi import APIRouter, Depends , status
from sqlalchemy.orm import Session
from src_code.utils.db import get_db
from src_code.vehicles.dtos import VehicleSchema, VehicleResponseSchema
from src_code.vehicles import controller
from src_code.users.models import UserModel
from src_code.users.controller import is_authenticated

vehicle_routes = APIRouter(prefix="/vehicles")

@vehicle_routes.post("/add", response_model=VehicleResponseSchema, status_code=status.HTTP_201_CREATED)
def add_vehicle(body:VehicleSchema,db:Session=Depends(get_db), user:UserModel = Depends(is_authenticated)):
    return controller.add_vehicle(body,db, user)



@vehicle_routes.get("/get_all", response_model=list[VehicleResponseSchema], status_code=status.HTTP_200_OK)
def get_all_vehicles(db:Session = Depends(get_db), user:UserModel = Depends(is_authenticated)):
    return controller.get_all_vehicles(db,user)



@vehicle_routes.get("/get/{vehicle_id}", response_model=VehicleResponseSchema, status_code=status.HTTP_200_OK)
def get_vehicle_by_id(vehicle_id: int, db: Session = Depends(get_db), user:UserModel = Depends(is_authenticated)):
    return controller.get_vehicle_by_id(vehicle_id,db, user)



@vehicle_routes.delete("/remove/{vehicle_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(vehicle_id: int,db: Session = Depends(get_db), user:UserModel = Depends(is_authenticated)):
    return controller.delete_vehicle(vehicle_id,db,user)