from __future__ import annotations
from pydantic import BaseModel
from app.models import Tree


class Plant(BaseModel):
    tree: "Tree"
    location: "Coordinate"
    


class Coordinate(BaseModel):
    latitude: float
    longitude: float


