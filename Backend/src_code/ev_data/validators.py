from fastapi import HTTPException


REQUIRED_COLUMNS = [
    "timestamp",
    "soc",
    "soh",
    "battery_voltage",
    "battery_current",
    "battery_temperature",
    "charge_cycles",
    "motor_temperature",
    "motor_vibration",
    "power_consumption",
    "ambient_temperature",
    "load_weight",
    "driving_speed",
    "distance_traveled",
    "motor_torque",
    "motor_rpm",
    "brake_pad_wear",
    "brake_pressure",
    "reg_brake_efficiency",
    "tire_pressure",
    "tire_temperature",
    "suspension_load",
    "ambient_humidity",
    "idle_time",
    "route_roughness",
    "maintenance_type"
]


class CSVValidator:


    @staticmethod
    def validate_file(file):

        if not file.filename.endswith(".csv"):
            raise ValueError(
                "Only CSV files are allowed"
            )

        if file.content_type != "text/csv":
            raise ValueError(
                "Invalid file type"
            )
        

    @staticmethod
    def validate_columns(df):

        missing_columns = []

        for column in REQUIRED_COLUMNS:

            if column not in df.columns:
                missing_columns.append(column)

        if missing_columns:
            raise ValueError(
                f"Missing columns: {missing_columns}"
            )



    @staticmethod
    def validate_empty(df):

        if df.empty:
            raise HTTPException(
                status_code=400,
                detail="Only CSV files are allowed"
            )