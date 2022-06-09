import sys
sys.path.append("..")
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..database import Base
from ..main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_export():
    response = client.post("/export")
    assert response.status_code == 200

def test_lookup_invalid_VIN_Special_Char():
    vin =  "1XPWD40X1ED21530!"
    response = client.get("/lookup/{}".format(vin))
    assert response.status_code == 400
    assert response.json() == {
        "detail" : "VIN is invalid."
    }

def test_lookup_invalid_VIN_less_than_17_chars():
    vin =  "1XPWD40X1ED21530"
    response = client.get("/lookup/{}".format(vin))
    assert response.status_code == 400
    assert response.json() == {
        "detail" : "VIN is invalid."
    }

def test_lookup_invalid_VIN_greater_than_17_chars():
    vin =  "1XPWD40X1ED2153000"
    response = client.get("/lookup/{}".format(vin))
    assert response.status_code == 400
    assert response.json() == {
        "detail" : "VIN is invalid."
    }

def test_lookup_vehicle_cache_vehicle_present():
    vin =  "4V4NC9EJXEN171694"
    response = client.get("/lookup/{}".format(vin))
    assert response.status_code == 200
    assert response.json() == {
        "vin": "4V4NC9EJXEN171694",
        "make": "VOLVO TRUCK",
        "model": "VNL",
        "model_year": "2014",
        "body_class": "Truck-Tractor",
        "cached_result": True
    }

def test_lookup_vehicle_cache_vehicle_absent():
    vin =  "1XPWD40X1ED215307"
    client.delete("/remove/{}".format(vin)) #remove entry from database if it exists. 

    response = client.get("/lookup/{}".format(vin))
    assert response.status_code == 200
    assert response.json() == {
        "vin": "1XPWD40X1ED215307",
        "make": "PETERBILT",
        "model": "388",
        "model_year": "2014",
        "body_class": "Truck-Tractor",
        "cached_result": False
    }

def test_lookup_no_such_vin():
    vin = "1234567891011ABCW"
    response = client.get("/lookup/{}".format(vin))
    assert response.status_code == 200
    assert response.json() == {"message": "No details exist for this VIN. Please try a different VIN"}

def test_remove_invalid_VIN_Special_Char():
    vin =  "1XPWD40X1ED21530!"
    response = client.delete("/remove/{}".format(vin))
    assert response.status_code == 400
    assert response.json() == {
        "detail" : "VIN is invalid."
    }

def test_remove_invalid_VIN_less_than_17_chars():
    vin =  "1XPWD40X1ED21530"
    response = client.delete("/remove/{}".format(vin))
    assert response.status_code == 400
    assert response.json() == {
        "detail" : "VIN is invalid."
    }

def test_remove_invalid_VIN_greater_than_17_chars():
    vin =  "1XPWD40X1ED2153000"
    response = client.delete("/remove/{}".format(vin))
    assert response.status_code == 400
    assert response.json() == {
        "detail" : "VIN is invalid."
    }

def test_remove_valid_VIN_present_in_cache():
    vin = "1XPWD40X1ED215307"
    response = client.delete("/remove/{}".format(vin))
    assert response.status_code == 200
    assert response.json() == {
        "vin": "1XPWD40X1ED215307",
        "cache_delete_success": True
    }

def test_remove_valid_VIN_absent_in_cache():
    vin = "1XP5DB9X7YN526158"
    response = client.delete("/remove/{}".format(vin))
    assert response.status_code == 200
    assert response.json() == {
        "vin": "1XP5DB9X7YN526158",
        "cache_delete_success": False
    }