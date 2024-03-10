import unittest
from datetime import datetime
from models.base_model import BaseModel
import time
""" Test suite for the BaseModel"""


class TestBaseModel(unittest.TestCase):
    """ Test suite """

    def setUp(self):
        """ set up testing model """
        self.my_model = BaseModel()

    def test_object_attributes(self):
        """ check public instance attributes values"""
        self.assertIsNotNone(self.my_model.id)
        self.assertIsInstance(self.my_model.created_at, datetime)
        self.assertIsInstance(self.my_model.updated_at, datetime)
        self.assertIsNone(self.my_model.my_number)
        self.assertIsNone(self.my_model.name)

    def test_string_representation_of_object(self):
        """ check string representation of object/class """
        expected_str = "[BaseModel] ({}) {}".format(
            self.my_model.id, self.my_model.__dict__)
        self.assertEqual(str(self.my_model), expected_str)

    def test_save_updates_updated_at(self):
        """ check if updated_at attribute gets
            updated every time a new object is created
        """
        initial_updated_at = self.my_model.updated_at
        time.sleep(1)
        self.my_model.save()
        self.assertNotEqual(self.my_model.updated_at, initial_updated_at)

    def test_to_dict_(self):
        """ check if dictionary contains the necessary keys """
        dict_representation = self.my_model.to_dict()
        expected_keys = ['id', 'created_at',
                         'updated_at', 'my_number', 'name', '__class__']

        for key in expected_keys:
            self.assertIn(key, dict_representation)

        self.assertEqual(dict_representation['__class__'], 'BaseModel')
        self.assertIsInstance(datetime.fromisoformat(
            dict_representation['created_at']), datetime)
        self.assertIsInstance(datetime.fromisoformat(
            dict_representation['updated_at']), datetime)

    def test_from_dict_with_datetime_conversion(self):
        """ check if we can re-create a class from a dict """
        my_model = BaseModel()
        my_model.name = "My_First_Model"
        my_model.my_number = 89

        my_model_json = my_model.to_dict()
        my_new_model = BaseModel(**my_model_json)

        self.assertEqual(my_model.id, my_new_model.id)
        self.assertEqual(my_model.name, my_new_model.name)
        self.assertEqual(my_model.my_number, my_new_model.my_number)

        self.assertIsInstance(my_new_model.created_at, datetime)
        self.assertIsInstance(my_new_model.updated_at, datetime)


if __name__ == '__main__':
    unittest.main()
