import logging
import sqlite3
import time

from fastapi import HTTPException
from schemas import InfoResponse

import pandas as pd

logger = logging.getLogger(__name__)

def export_cache_to_parquet_file(connection) -> InfoResponse:
    """This method exports the sqlite cache containing vehicle data to a parquet file.

    Args:
        conn (sqlite3.Connection): The Sqlite Connection object used to connect to the database.
    """
    try:
        df = pd.read_sql('SELECT * from vehicle', connection)
        filename = "vehicle_cache_" + time.strftime("%Y%m%d-%H%M%S")
        df.to_parquet(filename +  '.parquet', index = False)
        logger.info("%s exported successfully", filename)
        return {"message" : "Export Success."}
        
    except sqlite3.Error as error:
        logger.error("Error exporting parquet file ".join(error.args))
        raise HTTPException(status_code=400, detail='Error reading from db for export')