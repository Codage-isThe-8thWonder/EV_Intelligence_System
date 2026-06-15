from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src_code.users.models import UserModel
from src_code.vehicles.models import VehicleModel

from src_code.ev_data.models import EVDataModel
from src_code.ev_data.dtos import EVDataSchema

from src_code.ev_data.csv_processor import CSVProcessor
from src_code.ev_data.validators import CSVValidator
from src_code.ev_data.repository import EVDataRepository


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


def add_ev_data(
    body: EVDataSchema,
    db: Session,
    user: UserModel
):

    get_user_vehicle(
        body.vehicle_id,
        db,
        user
    )

    new_data = EVDataModel(
        **body.model_dump()
    )

    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return new_data


def get_all_ev_data(
    db: Session,
    user: UserModel
):

    records = (
        db.query(EVDataModel)
        .join(
            VehicleModel,
            VehicleModel.vehicle_id == EVDataModel.vehicle_id
        )
        .filter(
            VehicleModel.user_id == user.user_id
        )
        .all()
    )

    return records


def get_ev_data_by_id(
    data_id: int,
    db: Session,
    user: UserModel
):

    record = (
        db.query(EVDataModel)
        .join(
            VehicleModel,
            VehicleModel.vehicle_id == EVDataModel.vehicle_id
        )
        .filter(
            EVDataModel.data_id == data_id,
            VehicleModel.user_id == user.user_id
        )
        .first()
    )

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="EV data not found"
        )

    return record


def get_ev_data_by_vehicle(
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
        .all()
    )

    return records


def upload_csv(
    vehicle_id: int,
    file,
    db: Session,
    user: UserModel
):

    get_user_vehicle(
        vehicle_id,
        db,
        user
    )

    CSVValidator.validate_file(file)

    df = CSVProcessor.read_csv(
        file.file
    )

    CSVValidator.validate_empty(df)

    CSVValidator.validate_columns(df)

    df = CSVProcessor.clean_data(df)

    df = CSVProcessor.convert_types(df)

    records = []

    for _, row in df.iterrows():

        records.append(
            EVDataModel(
                vehicle_id=vehicle_id,

                timestamp=row["timestamp"],

                soc=row["soc"],
                soh=row["soh"],

                battery_voltage=row["battery_voltage"],
                battery_current=row["battery_current"],
                battery_temperature=row["battery_temperature"],

                charge_cycles=row["charge_cycles"],

                motor_temperature=row["motor_temperature"],
                motor_vibration=row["motor_vibration"],

                power_consumption=row["power_consumption"],

                ambient_temperature=row["ambient_temperature"],

                load_weight=row["load_weight"],

                driving_speed=row["driving_speed"],

                distance_traveled=row["distance_traveled"],

                motor_torque=row["motor_torque"],
                motor_rpm=row["motor_rpm"],

                brake_pad_wear=row["brake_pad_wear"],
                brake_pressure=row["brake_pressure"],
                reg_brake_efficiency=row["reg_brake_efficiency"],

                tire_pressure=row["tire_pressure"],
                tire_temperature=row["tire_temperature"],

                suspension_load=row["suspension_load"],

                ambient_humidity=row["ambient_humidity"],

                idle_time=row["idle_time"],

                route_roughness=row["route_roughness"],

                maintenance_type=row["maintenance_type"]
            )
        )

    EVDataRepository.bulk_insert(
        db,
        records
    )

    return {
        "rows_inserted": len(records)
    }