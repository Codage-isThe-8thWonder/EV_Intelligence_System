
from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from src_code.users.models import UserModel
from src_code.vehicles.models import VehicleModel
from src_code.ev_data.models import EVDataModel


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



def get_summary_card(
    vehicle_id: int,
    db: Session,
    user: UserModel
):

    get_user_vehicle(
        vehicle_id,
        db,
        user
    )

    summary = (
        db.query(
            func.avg(EVDataModel.soc).label("avg_soc"),

            func.avg(EVDataModel.soh).label("avg_soh"),

            func.max(
                EVDataModel.battery_temperature
            ).label(
                "max_battery_temperature"
            ),

            func.avg(
                EVDataModel.driving_speed
            ).label(
                "avg_driving_speed"
            ),

            func.sum(
                EVDataModel.distance_traveled
            ).label(
                "total_distance"
            ),

            func.avg(
                EVDataModel.power_consumption
            ).label(
                "avg_power_consumption"
            )

        )
        .filter(
            EVDataModel.vehicle_id == vehicle_id
        )
        .first()
    )

    if summary.avg_soc is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle data not found"
        )

    return {
        "avg_soc": summary.avg_soc,
        "avg_soh": summary.avg_soh,
        "max_battery_temperature":
            summary.max_battery_temperature,

        "avg_driving_speed":
            summary.avg_driving_speed,

        "total_distance":
            summary.total_distance,

        "avg_power_consumption":
            summary.avg_power_consumption
    }



def get_operational_trends(
    vehicle_id: int,
    db: Session,
    user: UserModel
):

    get_user_vehicle(
        vehicle_id,
        db,
        user
    )

    records = (
        db.query(EVDataModel)
        .filter(
            EVDataModel.vehicle_id == vehicle_id
        )
        .order_by(
            EVDataModel.timestamp
        )
        .all()
    )

    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle data not found"
        )

    soc_trend = []

    battery_temp_trend = []

    speed_trend = []

    power_trend = []

    motor_temp_trend = []

    for record in records:

        soc_trend.append(
            {
                "timestamp": record.timestamp,
                "value": record.soc
            }
        )

        battery_temp_trend.append(
            {
                "timestamp": record.timestamp,
                "value": record.battery_temperature
            }
        )

        speed_trend.append(
            {
                "timestamp": record.timestamp,
                "value": record.driving_speed
            }
        )

        power_trend.append(
            {
                "timestamp": record.timestamp,
                "value": record.power_consumption
            }
        )

        motor_temp_trend.append(
            {
                "timestamp": record.timestamp,
                "value": record.motor_temperature
            }
        )

    return {

        "soc": soc_trend,

        "battery_temperature": battery_temp_trend,

        "driving_speed": speed_trend,

        "power_consumption": power_trend,

        "motor_temperature": motor_temp_trend
    }



def get_battery_analytics(
    vehicle_id: int,
    db: Session,
    user: UserModel
):

    get_user_vehicle(
        vehicle_id,
        db,
        user
    )

    records = (
        db.query(EVDataModel)
        .filter(
            EVDataModel.vehicle_id == vehicle_id
        )
        .order_by(
            EVDataModel.timestamp
        )
        .all()
    )

    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle data not found"
        )

    soh_trend = []

    voltage_trend = []

    current_trend = []

    charge_cycle_trend = []

    for record in records:

        soh_trend.append(
            {
                "timestamp": record.timestamp,
                "value": record.soh
            }
        )

        voltage_trend.append(
            {
                "timestamp": record.timestamp,
                "value": record.battery_voltage
            }
        )

        current_trend.append(
            {
                "timestamp": record.timestamp,
                "value": record.battery_current
            }
        )

        charge_cycle_trend.append(
            {
                "timestamp": record.timestamp,
                "value": record.charge_cycles
            }
        )

    return {

        "soh": soh_trend,

        "battery_voltage": voltage_trend,

        "battery_current": current_trend,

        "charge_cycles": charge_cycle_trend
    }



def get_vehicle_performance(
    vehicle_id: int,
    db: Session,
    user: UserModel
):

    get_user_vehicle(
        vehicle_id,
        db,
        user
    )

    records = (
        db.query(EVDataModel)
        .filter(
            EVDataModel.vehicle_id == vehicle_id
        )
        .order_by(
            EVDataModel.timestamp
        )
        .all()
    )

    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle data not found"
        )

    distance_trend = []

    speed_vs_power = []

    ambient_vs_battery = []

    for record in records:

        distance_trend.append(
            {
                "timestamp": record.timestamp,
                "value": record.distance_traveled
            }
        )

        speed_vs_power.append(
            {
                "driving_speed": record.driving_speed,
                "power_consumption": record.power_consumption
            }
        )

        ambient_vs_battery.append(
            {
                "ambient_temperature": record.ambient_temperature,
                "battery_temperature": record.battery_temperature
            }
        )

    return {

        "distance_traveled": distance_trend,

        "speed_vs_power": speed_vs_power,

        "ambient_vs_battery_temperature": ambient_vs_battery
    }