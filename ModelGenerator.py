from textx import metamodel_from_file, metamodel_from_str, TextXSemanticError

from Classes.Robot import Robot
from Classes.Products import Products
from Classes.Property import Property


def check_inheritance(model, metamodel):
    if isinstance(model, Products):
        for robot in model.robots:
            if len(robot.name) == 0 or robot.name.isspace():
                raise TextXSemanticError('Name cannot be empty string.')

            if len(robot.inherits) != 0:

                if any([item == robot.name or len(robot.name) == 0 or robot.name.isspace() for item in robot.inherits]):
                    raise TextXSemanticError('Error in specifying inherited robots')

                names = [item.name for item in model.robots]
                is_inheritance_valid = [item in names for item in robot.inherits]

                if not all(is_inheritance_valid):
                    raise TextXSemanticError('Unknown object specified as inherited')
    else:
        if hasattr(model, 'name'):
            if len(model.name) == 0 or model.name.isspace():
                raise TextXSemanticError('Name cannot be empty string.')


def set_inheritance(products):
    for robot in products.robots:
        robot.inherit_properties(products.robots)


def extract_model_path(model_path):
    metamodel = metamodel_from_file('Grammar/RobotGrammar.tx', classes=[Property, Products, Robot])

    metamodel.register_obj_processors({'Products': set_inheritance})
    metamodel.register_model_processor(check_inheritance)

    model = metamodel.model_from_file(model_path)

    return model


def extract_model_string(model_string):
    metamodel = metamodel_from_file('Grammar/RobotGrammar.tx', classes=[Property, Products, Robot])

    metamodel.register_obj_processors({'Products': set_inheritance})
    metamodel.register_model_processor(check_inheritance)

    model = metamodel.model_from_str(model_string)

    return model
