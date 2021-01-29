from textx import metamodel_from_file, metamodel_from_str

from Classes.Robot import Robot
from Classes.Products import Products
from Classes.Property import Property


def set_inheritance(robot):
    robot.inherit_properties()


def extract_model_path(model_path):
    metamodel = metamodel_from_file('Grammar/RobotGrammar.tx', classes=[Property, Products, Robot])

    metamodel.register_obj_processors({'Robot': set_inheritance})

    model = metamodel.model_from_file(model_path)

    return model


def extract_model_string(model_string):
    metamodel = metamodel_from_file('Grammar/RobotGrammar.tx', classes=[Property, Products, Robot])

    metamodel.register_obj_processors({'Robot': set_inheritance})

    model = metamodel.model_from_str(model_string)

    return model
