import logging

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine
from export_cache import export_cache_to_parquet_file
from lookup import lookup_vehicle_cache, query_vpic_api, validate_vin
from remove_record import remove_cache_entry
from schemas import InfoResponse, RemoveResponse, VehicleResponse
from typing import Union

models.Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("app.log"),
                              logging.StreamHandler()])
app = FastAPI()

def get_db():
    """This method creates database session object to be used for db related operations.

    Yields:
        sessionmaker: The db session object to be used.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/export", response_model=InfoResponse)
def export(db: Session = Depends(get_db)):
    """This endpoint exports the sqlite db as a parquet file.

    Args:
        db (Session, optional): The db session required for connecting to the database.
    """
    engine = db.get_bind()
    return export_cache_to_parquet_file(engine)


@app.get("/lookup/{vin}", response_model= Union[VehicleResponse, InfoResponse], dependencies=[Depends(validate_vin)])
def lookup(vin: str, db: Session = Depends(get_db)):
    """This endpoint gets the vehicle details based on the provided VIN.

    Args:
        vin (str): The VIN of the vehicle which will be used for lookup.
        db (Session, optional): The db session required for connecting to the database.

    Returns:
        VehicleResponse: Response containing details of the vehicle.
    """
    vehicle = lookup_vehicle_cache(vin, db)
    if vehicle is not None:
        return vehicle
    else:
        return query_vpic_api(vin, db)


@app.delete("/remove/{vin}", response_model=RemoveResponse, dependencies=[Depends(validate_vin)])
def delete(vin: str, db: Session = Depends(get_db)):
    """This endpoint checks if a VIN entry is in the cache and if it is present, then removes it.

    Args:
        vin (str): VIN of the vehicle record to be removed from cache.
        db (Session, optional): The db session required for connecting to the database.

    Returns:
        RemoveResponse: The response type to be displayed. It contains 
    """
    return remove_cache_entry(vin, db)
