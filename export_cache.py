import logging
import os
import sqlite3
import time
from starlette.responses import FileResponse
from fastapi import HTTPException

import pandas as pd

logger = logging.getLogger(__name__)

def export_cache_to_parquet_file(connection) -> FileResponse:
    """This method exports the sqlite cache containing vehicle data to a parquet file.

    Args:
        conn (sqlite3.Connection): The Sqlite Connection object used to connect to the database.
    """
    try:
        df = pd.read_sql('SELECT * from vehicle', connection)
        filename = "vehicle_cache_" + time.strftime("%Y%m%d-%H%M%S") + '.parquet'
        dir = os.getcwd()
        file_path = os.path.join(dir, "export", filename)
        df.to_parquet(file_path, index = False)
        logger.info("%s exported successfully", filename)
        return FileResponse(file_path, media_type='application/octet-stream',filename="download.parquet")
        
    except sqlite3.Error as error:
        logger.error("Error exporting parquet file ".join(error.args))
        raise HTTPException(status_code=400, detail='Error reading from db for export')