from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from src_code.utils.db import get_db
from src_code.ev_data.dtos import EVDataSchema, EVDataResponseSchema
from src_code.ev_data import controller
from src_code.users.controller import is_authenticated
from src_code.users.models import UserModel

from fastapi import UploadFile, File


ev_data_routes = APIRouter(prefix="/ev-data")

@ev_data_routes.post("/add",response_model=EVDataResponseSchema,status_code=status.HTTP_201_CREATED)
def add_ev_data(body: EVDataSchema,db: Session = Depends(get_db),user: UserModel = Depends(is_authenticated)):
    return controller.add_ev_data(
        body,
        db,
        user
    )

@ev_data_routes.get("/get",response_model=list[EVDataResponseSchema])
def get_all_ev_data(db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)):
    return controller.get_all_ev_data(
        db,
        user
    )


@ev_data_routes.get("/get_ev/{data_id}",response_model=EVDataResponseSchema)
def get_ev_data_by_id(data_id: int,db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)):
    return controller.get_ev_data_by_id(
        data_id,
        db,
        user
    )


@ev_data_routes.get("/one_vehicle/{vehicle_id}",response_model=list[EVDataResponseSchema])
def get_ev_data_by_vehicle(vehicle_id: int,db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)):
    return controller.get_ev_data_by_vehicle(
        vehicle_id,
        db,
        user
    )



@ev_data_routes.post("/upload/{vehicle_id}")
def upload_csv(vehicle_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)):
    return controller.upload_csv(
        vehicle_id,
        file,
        db,
        user
    )