import pytest
from textx import TextXSyntaxError

from ModelGenerator import extract_model_string


def test_property_data_wrong_type_set():
    robot_model = """
        Item = asdf
    """

    with pytest.raises(TextXSyntaxError):
        extract_model_string(robot_model)


def test_property_data_no_value_set():
    robot_model = """
        Item = 
    """

    with pytest.raises(TextXSyntaxError):
        extract_model_string(robot_model)


def test_property_data_wrong_name_set():
    robot_model = """
        'Item' = 21
    """

    with pytest.raises(TextXSyntaxError):
        extract_model_string(robot_model)


def test_property_data_number_set():
    robot_model = """
        Item = 61.6
    """
    prop = extract_model_string(robot_model)
    assert prop.name == 'Item'
    assert prop.value == 61.6


def test_property_data_string_set():
    robot_model = """
        Item = 'random string'
    """
    prop = extract_model_string(robot_model)
    assert prop.name == 'Item'
    assert prop.value == 'random string'


def test_property_data_bool_set():
    robot_model = """
        Item = true
    """
    prop = extract_model_string(robot_model)
    assert prop.name == 'Item'
    assert prop.value


def test_robot_set_one_property():
    robot_model = """
    robot 'robot'{
        properties{
            Item1 = 126.712513
        }
    }
     """
    robot = extract_model_string(robot_model)
    assert len(robot.properties) == 1
    assert robot.properties[0].name == 'Item1'
    assert robot.properties[0].value == 126.712513


def test_robot_set_multi_property():
    robot_model = """
    robot 'robot'{
        properties{
            Item1 = 126.2
            Item2 = 'ajtem2'
            Item3 = false
        }
    }
     """
    robot = extract_model_string(robot_model)
    assert len(robot.properties) == 3
    assert robot.properties[0].name == 'Item1'
    assert robot.properties[0].value == 126.2
    assert robot.properties[1].name == 'Item2'
    assert robot.properties[1].value == 'ajtem2'
    assert robot.properties[2].name == 'Item3'
    assert not robot.properties[2].value


def test_multi_robot_set_multi_property():
    robot_model = """
    products {
        robot 'robot' {
            properties {
                Item4 = 01.1 //ZASTO????
                Item2 = 'ajtem1'
                Item3 = true
            }
        }
        robot 'robot2' {
            properties {
                Item1 = 2.1
                Item2 = 'ajtem2'
                Item3 = false
            }
        }
    }
     """
    products = extract_model_string(robot_model)

    assert len(products.robots) == 2
    for i in range(2):
        assert products.robots[i].properties[0].value == i + 1.1
        assert products.robots[i].properties[1].value == 'ajtem' + str(i + 1)
        assert products.robots[i].properties[2].value == (i == 0)
