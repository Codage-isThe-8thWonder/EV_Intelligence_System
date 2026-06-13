from fastapi import FastAPI
from src_code.utils.db import Base, engine
from src_code.vehicles.router import vehicle_routes
from src_code.vehicles.models import VehicleModel
from src_code.ev_data.router import ev_data_routes
from src_code.users.router import user_routes
from src_code.analytics.router import analytics_routes
from src_code.predictions.router import prediction_routes
from src_code.forecasting.router import forecast_routes
from src_code.recommendations.router import recommendations_routes

print(Base.metadata.tables.keys())
Base.metadata.create_all(engine)

app = FastAPI(title = "EV Intelligent Systems Platform")

app.include_router(vehicle_routes)
app.include_router(ev_data_routes)
app.include_router(user_routes)
app.include_router(analytics_routes)
app.include_router(prediction_routes)
app.include_router(forecast_routes)
app.include_router(recommendations_routes)
