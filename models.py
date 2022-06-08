from sqlalchemy import Column, String

from database import Base


class Vehicle(Base):
    """This class represents the table in the database.

    Args:
        Base (_type_): The Base type.
    """
    __tablename__ = "vehicle"

    vin = Column(String, primary_key=True, unique=True, index=True)
    make = Column(String)
    model = Column(String)
    model_year = Column(String)
    body_class = Column(String)
