from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src_code.users.models import UserModel
from src_code.vehicles.models import VehicleModel

from src_code.ev_data.models import EVDataModel

from src_code.predictions.controller import (
    get_predictions
)

from src_code.recommendations.dtos import (
    RecommendationResponse
)


def get_user_vehicle(
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



def get_recommendations(
    vehicle_id: int,
    db: Session,
    user: UserModel
):

    # Ownership verification
    get_user_vehicle(
        vehicle_id,
        db,
        user
    )

    latest_record = (
        db.query(EVDataModel)
        .filter(
            EVDataModel.vehicle_id == vehicle_id
        )
        .order_by(
            EVDataModel.timestamp.desc()
        )
        .first()
    )

    if latest_record is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No EV data found"
        )

    prediction = get_predictions(
        vehicle_id=vehicle_id,
        db=db,
        user=user
    )

    recommendations = []

    # SOC rules
    if latest_record.soc is not None and latest_record.soc < 20:

        recommendations.append(
            {
                "severity": "warning",
                "message": "Charge vehicle soon."
            }
        )

    # Battery temperature rules
    if (
        latest_record.battery_temperature is not None
        and
        latest_record.battery_temperature > 45
    ):

        recommendations.append(
            {
                "severity": "warning",
                "message": "Allow battery to cool before charging."
            }
        )

    # Motor temperature rules
    if (
        latest_record.motor_temperature is not None
        and
        latest_record.motor_temperature > 75
    ):

        recommendations.append(
            {
                "severity": "warning",
                "message": "Reduce aggressive driving and inspect motor system."
            }
        )

    # Health score rules
    if prediction.component_health_score < 70:

        recommendations.append(
            {
                "severity": "critical",
                "message": "Battery inspection recommended."
            }
        )

    # Failure probability rules
    if prediction.failure_probability > 0.80:

        recommendations.append(
            {
                "severity": "critical",
                "message": "Schedule maintenance immediately."
            }
        )

    # RUL rules
    if prediction.rul < 30:

        recommendations.append(
            {
                "severity": "critical",
                "message": "Component nearing end of useful life."
            }
        )

    # Everything normal
    if not recommendations:

        recommendations.append(
            {
                "severity": "info",
                "message": "Vehicle operating within normal conditions."
            }
        )

    return RecommendationResponse(
        vehicle_id=vehicle_id,
        recommendations=recommendations
    )