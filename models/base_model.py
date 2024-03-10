#!/usr/bin/python3
import uuid

""" class BaseModel that defines all common
    attributes/methods for other classes
 """
from datetime import datetime
import models


class BaseModel:
    """ BaseModael class """
    def __init__(self, *args, **kwargs):
        """ initialize BaseModel class """

        if kwargs:
            if "__class__" in kwargs:
                del kwargs["__class__"]

            for key, value in kwargs.items():
                setattr(self, key, value)
                if key == "updated_at" or key == "created_at":
                    setattr(self, key, datetime.strptime(
                        value, "%Y-%m-%dT%H:%M:%S.%f"))
        else:
            self.my_number = None
            self.name = None
            self.updated_at = datetime.now()
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """ string representation of BaseModel class """
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id,
                                     self.__dict__)

    def save(self):
        """ updates updated_at with current time """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """ returns dictionary representation of BaseModel class """
        dict_obj = self.__dict__.copy()
        dict_obj["__class__"] = self.__class__.__name__
        dict_obj["created_at"] = self.created_at.isoformat()
        dict_obj["updated_at"] = self.updated_at.isoformat()
        return dict_obj
