
from fastapi import HTTPException , status
from sqlalchemy.orm import Session
from src_code.vehicles.dtos import VehicleSchema
from src_code.vehicles.models import VehicleModel

def add_vehicle(body:VehicleSchema,db:Session):
    try:
        new_vehicle = VehicleModel(
            manufacturer=body.manufacturer,
            model=body.model
        )
        db.add(new_vehicle)
        db.commit()
        db.refresh(new_vehicle)
        return new_vehicle

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
