from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from src_code.utils.db import get_db
from src_code.ev_data.dtos import EVDataSchema, EVDataResponseSchema
from src_code.ev_data import controller


ev_data_routes = APIRouter(prefix="/ev-data")

@ev_data_routes.post("/add",response_model=EVDataResponseSchema,status_code=status.HTTP_201_CREATED)
def add_ev_data(body: EVDataSchema,db: Session = Depends(get_db)):
    return controller.add_ev_data(
        body,
        db
    )

@ev_data_routes.get("/get",response_model=list[EVDataResponseSchema])
def get_all_ev_data(db: Session = Depends(get_db)):
    return controller.get_all_ev_data(
        db
    )


@ev_data_routes.get("/get_ev/{data_id}",response_model=EVDataResponseSchema)
def get_ev_data_by_id(data_id: int,db: Session = Depends(get_db)):
    return controller.get_ev_data_by_id(
        data_id,
        db
    )


@ev_data_routes.get("/one_vehicle/{vehicle_id}",response_model=list[EVDataResponseSchema])
def get_ev_data_by_vehicle(vehicle_id: int,db: Session = Depends(get_db)):
    return controller.get_ev_data_by_vehicle(
        vehicle_id,
        db
    )

