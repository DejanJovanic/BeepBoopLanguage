import pytest
from textx import TextXSyntaxError

from ModelGenerator import extract_model_string


@pytest.fixture
def empty_products_correct():
    return """
    products { 

    }
    """


@pytest.fixture
def empty_robots_incorrect1():
    return """
    robot  { 

    }
    """


@pytest.fixture
def empty_robots_incorrect2():
    return """
    robot  { 
        properties{
        }
    }
    """


@pytest.fixture
def empty_robots_incorrect3():
    return """
      robot 'Robot' { 
      }
    """


@pytest.fixture
def empty_robots_correct_empty():
    return """
      robot 'Robot' { 
        properties {
        }
      }
    """


def test_empty_products_correct_set(empty_products_correct):
    model = extract_model_string(empty_products_correct)
    assert model
    assert not model.robots


def test_empty_robot_incorrect_set(empty_robots_incorrect1):
    with pytest.raises(TextXSyntaxError):
        extract_model_string(empty_robots_incorrect1)


def test_empty_robot_incorrect2(empty_robots_incorrect2):
    with pytest.raises(TextXSyntaxError):
        extract_model_string(empty_robots_incorrect2)


def test_empty_robot_correct_empty_set(empty_robots_correct_empty):
    model = extract_model_string(empty_robots_correct_empty)
    assert model
    assert not model.properties
