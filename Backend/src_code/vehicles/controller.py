
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src_code.users.models import UserModel
from src_code.vehicles.dtos import VehicleSchema
from src_code.vehicles.models import VehicleModel


def add_vehicle(
    body: VehicleSchema,
    db: Session,
    user: UserModel
):
    try:

        new_vehicle = VehicleModel(
            user_id=user.user_id,
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


def get_all_vehicles(
    db: Session,
    user: UserModel
):

    vehicles = (
        db.query(VehicleModel)
        .filter(
            VehicleModel.user_id == user.user_id
        )
        .all()
    )

    return vehicles


def get_vehicle_by_id(
    vehicle_id: int,
    db: Session,
    user: UserModel
):

    vehicle = (
        db.query(VehicleModel)
        .filter(
            VehicleModel.vehicle_id == vehicle_id,
            VehicleModel.user_id == user.user_id
        )
        .first()
    )

    if vehicle is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )

    return vehicle


def delete_vehicle(
    vehicle_id: int,
    db: Session,
    user: UserModel
):

    vehicle = (
        db.query(VehicleModel)
        .filter(
            VehicleModel.vehicle_id == vehicle_id,
            VehicleModel.user_id == user.user_id
        )
        .first()
    )

    if vehicle is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )

    db.delete(vehicle)
    db.commit()

    return None