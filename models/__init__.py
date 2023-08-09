#!/usr/bin/python3
"""__init__ The magic method for models directory..."""
from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
