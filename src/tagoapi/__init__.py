from ._version import __version__
from .client import TAGOClient
from .station_catalog import StationCatalog
from .models import ArrivalInfo, BaseModel, CityCode, Route, Station, Vehicle
from .resources import (
    ArrivalResource,
    CityResource,
    RouteResource,
    StationResource,
    TagoPage,
    VehicleResource,
)

__all__ = [
    "TAGOClient",
    "StationCatalog",
    "__version__",
    "BaseModel",
    "Route",
    "Vehicle",
    "Station",
    "ArrivalInfo",
    "CityCode",
    "TagoPage",
    "RouteResource",
    "StationResource",
    "ArrivalResource",
    "VehicleResource",
    "CityResource",
]
