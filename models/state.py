#!/usr/bin/python3
"""Defines State class."""
from models.base_model import BaseModel


class State(BaseModel):
    """Represent a state.

    Attributes:
        name (str): The state name.
    """

    name = ""
