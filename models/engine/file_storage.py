#!/usr/bin/python3
"""Defines FileStorage class..."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Represents the abstracted storage engine.

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id"""
        newname1 = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(newname1, obj.id)] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        odict1 = FileStorage.__objects
        objdict1 = {obj: odict1[obj].to_dict() for obj in odict1.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(objdict1, f)

    def reload(self):
        """Deserialize JSON file __file_path to __objects, if it exists."""
        try:
            with open(FileStorage.__file_path) as f:
                objdict1 = json.load(f)
                for z in objdict1.values():
                    cls_name = z["__class__"]
                    del z["__class__"]
                    self.new(eval(cls_name)(**z))
        except FileNotFoundError:
            return
