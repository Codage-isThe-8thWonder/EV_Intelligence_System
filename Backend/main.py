from fastapi import FastAPI
from src_code.utils.db import Base, engine
from src_code.vehicles.router import vehicle_routes
from src_code.vehicles.models import VehicleModel


print(Base.metadata.tables.keys())
Base.metadata.create_all(engine)

app = FastAPI(title="EV Intelligent Systems Platform")

app.include_router(vehicle_routes)
