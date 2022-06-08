import logging

from pydantic import BaseModel
from sqlalchemy.orm import Session

from models import Vehicle
from schemas import RemoveResponse

logger = logging.getLogger(__name__)


def remove_cache_entry(vin : str , db : Session) -> RemoveResponse:
    """This method checks if the entry is present in the db. If it is, then it removes it.

    Args:
        vin (str): VIN of the vehicle record to be removed from cache.
        db (Session): The db session required for connecting to the database.

    Returns:
        RemoveResponse: The response to be sent to the endpoint.
    """
    result = db.query(Vehicle).filter(Vehicle.vin == vin).delete()
    if result == 1:
        db.commit()
        logger.info("%s deleted from SQLite Database", vin)
        return {"vin": vin, "cache_delete_success": True}
    else:
        logger.info("%s not found in SQLite Database", vin)
        return {"vin": vin, "cache_delete_success": False}
