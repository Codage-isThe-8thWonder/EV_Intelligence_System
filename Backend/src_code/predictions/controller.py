from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src_code.predictions.dtos import PredictionResponseDTO
from src_code.ev_data.models import EVDataModel
from src_code.vehicles.models import VehicleModel
from src_code.users.models import UserModel

import pandas as pd
import joblib


RUL_MODEL = joblib.load(
    "src_code/ML_part/saved_models/rul_model.pkl"
)

FAILURE_MODEL = joblib.load(
    "src_code/ML_part/saved_models/failure_probability_model.pkl"
)

HEALTH_MODEL = joblib.load(
    "src_code/ML_part/saved_models/component_health_model.pkl"
)


def calculate_driving_range(
    soc: float,
    battery_capacity: float,
    power_consumption: float
):

    if power_consumption <= 0:
        return 0.0

    available_energy = (
        battery_capacity * (soc / 100)
    )

    estimated_range = (
        available_energy / power_consumption
    ) * 100

    return round(
        estimated_range,
        2
    )


def calculate_charging_time(
    soc: float,
    battery_capacity: float
):

    charger_power = 7.2

    required_energy = (
        battery_capacity *
        ((100 - soc) / 100)
    )

    charging_time_hours = (
        required_energy / charger_power
    )

    return round(
        charging_time_hours,
        2
    )


def get_predictions(
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

    records = (
        db.query(EVDataModel)
        .filter(
            EVDataModel.vehicle_id == vehicle_id
        )
        .order_by(
            EVDataModel.timestamp.desc()
        )
        .limit(20)
        .all()
    )

    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No EV data found"
        )

    if vehicle.battery_capacity is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Battery capacity not configured"
        )

    df = pd.DataFrame([
        {
            "soc": r.soc,
            "soh": r.soh,

            "battery_voltage": r.battery_voltage,
            "battery_current": r.battery_current,
            "battery_temperature": r.battery_temperature,

            "charge_cycles": r.charge_cycles,

            "motor_temperature": r.motor_temperature,
            "motor_vibration": r.motor_vibration,

            "power_consumption": r.power_consumption,

            "ambient_temperature": r.ambient_temperature,

            "load_weight": r.load_weight,

            "driving_speed": r.driving_speed,

            "distance_traveled": r.distance_traveled,

            "motor_torque": r.motor_torque,
            "motor_rpm": r.motor_rpm,

            "brake_pad_wear": r.brake_pad_wear,
            "brake_pressure": r.brake_pressure,

            "reg_brake_efficiency": r.reg_brake_efficiency,

            "tire_pressure": r.tire_pressure,
            "tire_temperature": r.tire_temperature,

            "suspension_load": r.suspension_load,

            "ambient_humidity": r.ambient_humidity,

            "idle_time": r.idle_time,

            "route_roughness": r.route_roughness,

            "maintenance_type": r.maintenance_type
        }

        for r in records
    ])

    feature_df = pd.DataFrame(
        [df.mean()]
    )

    soc = feature_df["soc"].iloc[0]

    power_consumption = (
        feature_df["power_consumption"]
        .iloc[0]
    )

    rul = float(
        RUL_MODEL.predict(feature_df)[0]
    )

    failure_probability = float(
        FAILURE_MODEL
        .predict_proba(feature_df)[0][1]
    )

    health_score = float(
        HEALTH_MODEL.predict(feature_df)[0]
    )

    estimated_range = (
        calculate_driving_range(
            soc=soc,
            battery_capacity=vehicle.battery_capacity,
            power_consumption=power_consumption
        )
    )

    estimated_charging_time = (
        calculate_charging_time(
            soc=soc,
            battery_capacity=vehicle.battery_capacity
        )
    )

    return PredictionResponseDTO(
        rul=rul,
        failure_probability=failure_probability,
        component_health_score=health_score,
        estimated_driving_range=estimated_range,
        estimated_charging_time=estimated_charging_time
    )