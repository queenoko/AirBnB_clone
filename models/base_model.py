#!/usr/bin/python3
"""The BaseModel class."""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Represents BaseModel of AirBnB project..."""

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel.

        Args:
            *args (any): domant.
            **kwargs (dict): Key/value pairs of attributes.
        """
        tform = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for y, v in kwargs.items():
                if y == "created_at" or y == "updated_at":
                    self.__dict__[y] = datetime.strptime(v, tform)
                else:
                    self.__dict__[y] = v
        else:
            models.storage.new(self)

    def save(self):
        """Update updated_at with current datetime."""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """Return the dictionary of the BaseModel instance.

        Includes the key/value pair __class__ representing
        the class name of the object.
        """
        copy_dict1 = self.__dict__.copy()
        copy_dict1["created_at"] = self.created_at.isoformat()
        copy_dict1["updated_at"] = self.updated_at.isoformat()
        copy_dict1["__class__"] = self.__class__.__name__
        return copy_dict1

    def __str__(self):
        """Return the print/str representation of the BaseModel instance."""
        cls_name = self.__class__.__name__
        return "[{}] ({}) {}".format(cls_name, self.id, self.__dict__)
