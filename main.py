from textx import metamodel_from_file

from Classes.Robot import Robot
from Classes.Products import Products
from Classes.Property import Property


def set_inheritance(robot):
    robot.inherit_properties()


def main():
    metamodel = metamodel_from_file('Grammar/RobotGrammar.tx', classes=[Property, Products, Robot])

    metamodel.register_obj_processors({'Robot': set_inheritance})

    model = metamodel.model_from_file('Models/Robots.model')

    b = model


if __name__ == "__main__":
    main()
