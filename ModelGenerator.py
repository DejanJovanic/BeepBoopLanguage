from textx import metamodel_from_file, TextXSemanticError

from Classes.Robot import Robot
from Classes.Products import Products
from Classes.Property import Property


def check_name(model):
    if len(model.name) == 0 or model.name.isspace():
        raise TextXSemanticError('Name cannot be empty string.')


def check_inherited_name(robot):
    if any([item == robot.name or len(robot.name) == 0 or robot.name.isspace() for item in robot.inherits]):
        raise TextXSemanticError('Error in specifying inherited robots')


def check_if_inherited_exists(robot, robots):
    names = [item.name for item in robots]
    is_inheritance_valid = [item in names for item in robot.inherits]

    if not all(is_inheritance_valid):
        raise TextXSemanticError('Unknown object specified as inherited')


def set_inheritance(products):
    for robot in products.robots:
        robot.inherit_properties(products.robots)


def check_model_and_set_inheritance(model, metamodel):
    if isinstance(model, Products):
        for robot in model.robots:
            check_name(robot)
            if len(robot.inherits) != 0:
                check_inherited_name(robot)
                check_if_inherited_exists(robot, model.robots)

        set_inheritance(model)
    else:
        if hasattr(model, 'name'):
            check_name(model)


def extract_model_path(model_path):
    metamodel = metamodel_from_file('Grammar/RobotGrammar.tx', classes=[Property, Products, Robot])

    metamodel.register_model_processor(check_model_and_set_inheritance)

    model = metamodel.model_from_file(model_path)

    return model


def extract_model_string(model_string):
    metamodel = metamodel_from_file('Grammar/RobotGrammar.tx', classes=[Property, Products, Robot])

    metamodel.register_model_processor(check_model_and_set_inheritance)

    model = metamodel.model_from_str(model_string)

    return model
