from fastapi import HTTPException
from sqlalchemy.orm import Session

from src_code.ev_data.models import EVDataModel
from src_code.ev_data.dtos import EVDataSchema


def add_ev_data(body: EVDataSchema,db: Session):
    new_data = EVDataModel(**body.model_dump())

    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return new_data


def get_all_ev_data(db: Session):

    return db.query(EVDataModel).all()


def get_ev_data_by_id(data_id: int,db: Session):

    record = db.query(EVDataModel).filter(EVDataModel.data_id == data_id).first()
    if not record:
        raise HTTPException(
            status_code=404,
            detail="EV data not found"
        )

    return record


def get_ev_data_by_vehicle(vehicle_id: int,db: Session):

    records = db.query(EVDataModel).filter(EVDataModel.vehicle_id == vehicle_id).all()

    return records