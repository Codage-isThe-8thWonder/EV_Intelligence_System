import joblib
import numpy as np
from tensorflow.keras.models import load_model
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src_code.ev_data.models import EVDataModel
from src_code.forecasting.dtos import ForecastResponse, ForecastValues



SOC_MODEL = load_model(
    "src_code/ML_part/notebooks/Forecasting models/soc_forecast_model.keras"
)

VOLTAGE_MODEL = load_model(
    "src_code/ML_part/notebooks/Forecasting models/voltage_forecast_model.keras"
)

SOC_FEATURE_SCALER = joblib.load(
    "src_code/ML_part/notebooks/Forecasting models/soc_feature_scaler.pkl"
)

SOC_TARGET_SCALER = joblib.load(
    "src_code/ML_part/notebooks/Forecasting models/soc_target_scaler.pkl"
)

VOLTAGE_FEATURE_SCALER = joblib.load(
    "src_code/ML_part/notebooks/Forecasting models/voltage_feature_scaler.pkl"
)

VOLTAGE_TARGET_SCALER = joblib.load(
    "src_code/ML_part/notebooks/Forecasting models/voltage_target_scaler.pkl"
)





def get_forecast(vehicle_id: int, db: Session):

    try:

        records = db.query(EVDataModel).filter(EVDataModel.vehicle_id == vehicle_id).order_by(EVDataModel.timestamp.desc()).limit(24).all()

        if len(records) < 24:
            raise HTTPException(
                status_code=400,
                detail="Need at least 24 records"
            )
        
        records.reverse()

        sequence = []
        for row in records:
            sequence.append([
                row.soc,
                row.soh,
                row.battery_voltage,
                row.battery_current,
                row.power_consumption,
                row.driving_speed
            ])

        sequence = np.array(sequence,dtype=np.float32)


        soc_input = SOC_FEATURE_SCALER.transform(sequence)
        soc_input = soc_input.reshape(1,sequence.shape[0],sequence.shape[1])
        soc_prediction = SOC_MODEL.predict(soc_input,verbose=0)
        soc_prediction = (SOC_TARGET_SCALER.inverse_transform(soc_prediction))[0]


        voltage_input = VOLTAGE_FEATURE_SCALER.transform(sequence)
        voltage_input = voltage_input.reshape(1,sequence.shape[0],sequence.shape[1])
        voltage_prediction = VOLTAGE_MODEL.predict(voltage_input,verbose=0)
        voltage_prediction = (VOLTAGE_TARGET_SCALER.inverse_transform(voltage_prediction))[0]


        return ForecastResponse(

                vehicle_id=vehicle_id,

                soc_forecast=ForecastValues(
                    one_hour=float(
                        soc_prediction[0]
                    ),
                    six_hours=float(
                        soc_prediction[1]
                    ),
                    twenty_four_hours=float(
                        soc_prediction[2]
                    )
                ),

                voltage_forecast=ForecastValues(
                    one_hour=float(
                        voltage_prediction[0]
                    ),
                    six_hours=float(
                        voltage_prediction[1]
                    ),
                    twenty_four_hours=float(
                        voltage_prediction[2]
                    )
                )
            )
    
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Forecast generation failed: {str(e)}"
        )




