
from fastapi import HTTPException , status
from sqlalchemy.orm import Session
from src_code.vehicles.dtos import VehicleSchema
from src_code.vehicles.models import VehicleModel

def add_vehicle(body:VehicleSchema,db:Session):
    try:
        new_vehicle = VehicleModel(
            manufacturer=body.manufacturer,
            model=body.model,
            nickname=body.nickname,
            battery_capacity=body.battery_capacity
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



def get_all_vehicles(db: Session):
    vehicles = db.query(VehicleModel).all()
    return vehicles



def get_vehicle_by_id(vehicle_id: int, db: Session):
    vehicle = db.query(VehicleModel).get(vehicle_id)

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    return vehicle



def delete_vehicle(vehicle_id: int, db: Session):
    vehicle = db.query(VehicleModel).filter(
        VehicleModel.vehicle_id == vehicle_id
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    db.delete(vehicle)
    db.commit()

    return {
        "message": "Vehicle deleted successfully"
    }