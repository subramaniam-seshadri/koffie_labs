import json
import logging
from typing import Dict, Union

import requests
from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Vehicle
from schemas import InfoResponse, VehicleResponse

logger = logging.getLogger(__name__)

url = 'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValuesBatch/';

def get_vehicle_by_vin(vin: str, db: Session) -> Union[Vehicle, None]:
    """This method searches for the Vehicle record in the cache. Searching is done based on the VIN provided.

    Args:
        vin (str): The VIN of the vehicle which will be used for lookup.
        db (Session): The db session required for connecting to the database.

    Returns:
        Union[Vehicle, None]: Returns the Vehicle object if it is present in cache otherwise returns None.
    """
    return db.query(Vehicle).filter(Vehicle.vin == vin).first()


def validate_vin(vin : str) -> None:
    """This method validates the VIN of the vehicle to be queried. 

    Args:
        vin (str): The VIN of the vehicle which will be used for lookup.

    Raises:
        HTTPException: Returns an error if VIN is invalid.
    """
    if len(vin) != 17 or (not str.isalnum(vin)):
        logger.error("User entered invalid VIN - %s", vin)
        raise HTTPException(status_code=400, detail='VIN is invalid.')


def lookup_vehicle_cache(vin: str, db: Session) -> Union[VehicleResponse, None]:
    """This method generates the response to be sent to the endpoint.

    Args:
        vin (str): The VIN of the vehicle which will be used for lookup.
        db (Session): The db session required for connecting to the database.

    Returns:
        Union[VehicleResponse, None]: Returns the VehicleResponse object if it is present in cache otherwise returns None.
    """
    vehicle = get_vehicle_by_vin(vin, db)
    if vehicle is not None:
        logger.info("%s found in cache.", vehicle.vin)
        return {"vin": vehicle.vin, "make" : vehicle.make, "model" : vehicle.model, 
        "model_year": vehicle.model_year, "body_class" : vehicle.body_class, "cached_result": True}
    else: 
        return None


def query_vpic_api(vin : str, db: Session) -> Union[VehicleResponse, InfoResponse]:
    """This method queries the vpic api to get the details of the vehicle.

    Args:
        vin (str): The VIN of the vehicle which will be used for lookup.
        db (Session): The db session required for connecting to the database.

    Returns:
        Union[VehicleResponse, None]: Returns the VehicleResponse object or None.
    """
    logger.info("%s not found in cache. Querying VPIC API.", vin)
    post_fields = {'format': 'json', 'data': vin}
    response = requests.post(url, data=post_fields)
    if response is not None:
        response_dict = json.loads(response.text)
        if response_dict["Count"] == 1 and response_dict["Results"][0]["Make"] != "" and response_dict["Results"][0]["Model"] != "":
            response_dict = response_dict["Results"][0]
            vehicle = VehicleResponse(vin=response_dict["VIN"], make=response_dict["Make"], model=response_dict["Model"], model_year=response_dict["ModelYear"], body_class=response_dict["BodyClass"], cached_result=False)
            logger.info("Inserting %s record into db.", vin)
            insert_into_cache(response_dict, db)
            return vehicle
        else:
            logger.info("No details for %s VIN", vin)
            return {"message": "No details exist for this VIN. Please try a different VIN"}
    else:
        logger.info("No response from VPIC API for %s VIN", vin)
        return {"message" : "No response from VPIC API. Please try again later"}


def insert_into_cache(vehicle_dict : Dict, db: Session):
    """This method inserts the vehicle details queried from VPIC API into db cache.

    Args:
        vehicle_dict (Dict): A dictionary containing the vehicle details.
        db (Session): The db session required for connecting to the database.
    """
    vehicle = Vehicle(vin = vehicle_dict["VIN"], make=vehicle_dict["Make"], model=vehicle_dict["Model"], model_year=vehicle_dict["ModelYear"], body_class=vehicle_dict["BodyClass"])
    db.add(vehicle)
    db.commit()
