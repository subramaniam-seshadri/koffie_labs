from pydantic import BaseModel


class Vehicle():
    """This class represents the type that gets mapped from the table. 
    """
    vin : str
    make : str
    model : str
    model_year : str
    body_class : str

    class Config:
        orm_mode = True


class VehicleResponse(BaseModel):
    """This type represents the response to be sent to the endpoint to display vehicle details.

    Args:
        BaseModel (_type_): The Base model to inherit pydantic properties.
    """
    vin : str
    make : str
    model : str
    model_year : str
    body_class : str
    cached_result : bool


class RemoveResponse(BaseModel):
    """The response type to be sent to the endpoint.

    Args:
        BaseModel (BaseModel): The BaseModel type to be inherited from pydantic.
    """
    vin: str
    cache_delete_success : bool


class InfoResponse(BaseModel):
    """Generic message to be displayed to the user.

    Args:
        BaseModel (BaseModel): The BaseModel type to be inherited from pydantic.
    """
    message : str