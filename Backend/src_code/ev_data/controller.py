from fastapi import HTTPException
from sqlalchemy.orm import Session

from src_code.ev_data.models import EVDataModel
from src_code.ev_data.dtos import EVDataSchema

from src_code.ev_data.csv_processor import CSVProcessor
from src_code.ev_data.validators import CSVValidator
from src_code.ev_data.repository import EVDataRepository


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




def upload_csv(vehicle_id,file,db):

    CSVValidator.validate_file(file)

    df = CSVProcessor.read_csv(file.file)

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

                distance_traveled=row["distance_traveled"]
            )
        )

    EVDataRepository.bulk_insert(
        db,
        records
    )

    return {
        "rows_inserted": len(records)
    }