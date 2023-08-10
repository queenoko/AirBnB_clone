#!/usr/bin/python3
"""Defines City class..."""
from models.base_model import BaseModel


class City(BaseModel):
    """Represent a city.

    Attributes:
        state_id (str): State id.
        name (str): The name of city.
    """

    state_id = ""
    name = ""
