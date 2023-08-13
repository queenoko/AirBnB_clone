#!/usr/bin/python3
"""Defines the  unittests for models/base_model.py...

Unittest classes:
    TestBaseModel_instantiation
    TestBaseModel_save
    TestBaseModel_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_instantiation(unittest.TestCase):
    """Unittest for testing instantiation of BaseModel class."""

    def test_no_args_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_unique_ids(self):
        bam1 = BaseModel()
        bam2 = BaseModel()
        self.assertNotEqual(bam1.id, bam2.id)

    def test_two_models_different_created_at(self):
        bam1 = BaseModel()
        sleep(0.05)
        bam2 = BaseModel()
        self.assertLess(bam1.created_at, bam2.created_at)

    def test_two_models_different_updated_at(self):
        bam1 = BaseModel()
        sleep(0.05)
        bam2 = BaseModel()
        self.assertLess(bam1.updated_at, bam2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        bam = BaseModel()
        bam.id = "123456"
        bam.created_at = bam.updated_at = dt
        bamstr = bam.__str__()
        self.assertIn("[BaseModel] (123456)", bamstr)
        self.assertIn("'id': '123456'", bamstr)
        self.assertIn("'created_at': " + dt_repr, bamstr)
        self.assertIn("'updated_at': " + dt_repr, bamstr)

    def test_args_unused(self):
        bam = BaseModel(None)
        self.assertNotIn(None, bam.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bam = BaseModel(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(bam.id, "345")
        self.assertEqual(bam.created_at, dt)
        self.assertEqual(bam.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bm = BaseModel("12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(bam.id, "345")
        self.assertEqual(bam.created_at, dt)
        self.assertEqual(bam.updated_at, dt)


class TestBaseModel_save(unittest.TestCase):
    """Unittests for testing save method of the BaseModel class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        bam = BaseModel()
        sleep(0.05)
        first_updated_at = bm.updated_at
        bam.save()
        self.assertLess(first_updated_at, bm.updated_at)

    def test_two_saves(self):
        bam = BaseModel()
        sleep(0.05)
        first_updated_at = bam.updated_at
        bam.save()
        second_updated_at = bam.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        bam.save()
        self.assertLess(second_updated_at, bm.updated_at)

    def test_save_with_arg(self):
        bam = BaseModel()
        with self.assertRaises(TypeError):
            bam.save(None)

    def test_save_updates_file(self):
        bam = BaseModel()
        bam.save()
        bamid = "BaseModel." + bam.id
        with open("file.json", "r") as f:
            self.assertIn(bamid, f.read())


class TestBaseModel_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the BaseModel class."""

    def test_to_dict_type(self):
        bam = BaseModel()
        self.assertTrue(dict, type(bam.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        bam = BaseModel()
        self.assertIn("id", bam.to_dict())
        self.assertIn("created_at", bam.to_dict())
        self.assertIn("updated_at", bam.to_dict())
        self.assertIn("__class__", bam.to_dict())

    def test_to_dict_contains_added_attributes(self):
        bam = BaseModel()
        bam.name = "Holberton"
        bam.my_number = 98
        self.assertIn("name", bam.to_dict())
        self.assertIn("my_number", bam.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        bam = BaseModel()
        bam_dict = bam.to_dict()
        self.assertEqual(str, type(bam_dict["created_at"]))
        self.assertEqual(str, type(bam_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        bam = BaseModel()
        bam.id = "123456"
        bam.created_at = bam.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat()
        }
        self.assertDictEqual(bm.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        bam = BaseModel()
        self.assertNotEqual(bam.to_dict(), bam.__dict__)

    def test_to_dict_with_arg(self):
        bam = BaseModel()
        with self.assertRaises(TypeError):
            bam.to_dict(None)


if __name__ == "__main__":
    unittest.main()
