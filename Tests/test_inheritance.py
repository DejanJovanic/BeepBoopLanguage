import pytest
from textx import TextXSemanticError

from ModelGenerator import extract_model_string


def test_inheritance_wrong_name():
    robot_model = """
      products {
          robot 'robot' {
              properties {
                  Item1 = 6.1 
                  Item2 = 'ajtem1'
                  Item3 = true
              }
          }
          robot 'robot2'  {
              properties inherits from 'definitely_not_robot' {
                  Item1 = 2.1
                  Item2 = 'ajtem2'
                  Item3 = false
              }
          }
      }
       """
    with pytest.raises(TextXSemanticError):
        extract_model_string(robot_model)


def test_inheritance_one_item_different_properties():
    robot_model = """
      products {
          robot 'robot' {
              properties {
                  Item1 = 6.2
                  Item2 = 'ajtem1'
                  Item3 = true
              }
          }
          robot 'robot2'  {
              properties inherits from 'robot' {
                  Item4 = 2.1
                  Item5 = 'ajtem2'
                  Item6 = false
              }
          }
      }
       """
    products = extract_model_string(robot_model)

    assert len(products.robots) == 2
    # Robot1
    assert len(products.robots[0].properties) == 3

    assert products.robots[0].properties[0].name == 'Item1' and products.robots[0].properties[0].value == 6.2
    assert products.robots[0].properties[1].name == 'Item2' and products.robots[0].properties[1].value == 'ajtem1'
    assert products.robots[0].properties[2].name == 'Item3' and products.robots[0].properties[2].value
    # Robot2
    assert len(products.robots[1].properties) == 6

    assert products.robots[1].inherits[0] == products.robots[0].name

    assert products.robots[1].properties[3].name == 'Item1' and products.robots[1].properties[3].value == 6.2
    assert products.robots[1].properties[4].name == 'Item2' and products.robots[1].properties[4].value == 'ajtem1'
    assert products.robots[1].properties[5].name == 'Item3' and products.robots[1].properties[5].value

    assert products.robots[1].properties[0].name == 'Item4' and products.robots[1].properties[0].value == 2.1
    assert products.robots[1].properties[1].name == 'Item5' and products.robots[1].properties[1].value == 'ajtem2'
    assert products.robots[1].properties[2].name == 'Item6' and not products.robots[1].properties[2].value


def test_inheritance_multiple_items_different_properties_start():
    robot_model = """
      products {
          robot 'robot' {
              properties inherits from 'robot2', 'robot3'  {
                  Item1 = 6.2
              }
          }
          robot 'robot2'  {
              properties {
                  Item2 = true
              }
          }
          robot 'robot3'  {
              properties  {
                  Item3 = 'atribut'
              }
          }
      }
       """
    products = extract_model_string(robot_model)

    assert len(products.robots[0].properties) == 3

    assert products.robots[0].properties[0].name == 'Item1' and products.robots[0].properties[0].value == 6.2
    assert products.robots[0].properties[1].name == 'Item2' and products.robots[0].properties[1].value
    assert products.robots[0].properties[2].name == 'Item3' and products.robots[0].properties[2].value == 'atribut'


def test_inheritance_multiple_items_different_properties_middle():
    robot_model = """
      products {
          robot 'robot' {
              properties {
                  Item1 = 6.2
              }
          }
          robot 'robot2' {
              properties inherits from 'robot', 'robot3'  {
                  Item2 = true
              }
          }
          robot 'robot3'  {
              properties  {
                  Item3 = 'atribut'
              }
          }
      }
       """
    products = extract_model_string(robot_model)

    assert len(products.robots[1].properties) == 3

    assert products.robots[1].properties[1].name == 'Item1' and products.robots[1].properties[1].value == 6.2
    assert products.robots[1].properties[0].name == 'Item2' and products.robots[1].properties[0].value
    assert products.robots[1].properties[2].name == 'Item3' and products.robots[1].properties[2].value == 'atribut'


def test_inheritance_multiple_items_different_properties_end():
    robot_model = """
      products {
          robot 'robot' {
              properties   {
                  Item1 = 6.2
              }
          }
          robot 'robot2'  {
              properties {
                  Item2 = true
              }
          }
          robot 'robot3'  {
              properties inherits from 'robot','robot2'  {
                  Item3 = 'atribut'
              }
          }
      }
       """
    products = extract_model_string(robot_model)

    assert len(products.robots[2].properties) == 3

    assert products.robots[2].properties[1].name == 'Item1' and products.robots[2].properties[1].value == 6.2
    assert products.robots[2].properties[2].name == 'Item2' and products.robots[2].properties[2].value
    assert products.robots[2].properties[0].name == 'Item3' and products.robots[2].properties[0].value == 'atribut'


def test_inheritance_multiple_items_same_properties_end():
    robot_model = """
      products {
          robot 'robot' {
              properties   {
                  Item1 = 6.2
              }
          }
          robot 'robot2'  {
              properties {
                  Item1 = 7.21
              }
          }
          robot 'robot3'  {
              properties inherits from 'robot','robot2'  {
                  Item3 = 'atribut'
              }
          }
      }
       """
    products = extract_model_string(robot_model)

    assert len(products.robots[2].properties) == 2

    assert products.robots[2].properties[1].name == 'Item1' and products.robots[2].properties[1].value == 6.2
    assert products.robots[2].properties[0].name == 'Item3' and products.robots[2].properties[0].value == 'atribut'


def test_inheritance_multiple_items_same_properties_end2():
    robot_model = """
      products {
          robot 'robot' {
              properties   {
                  Item1 = 6.2
              }
          }
          robot 'robot2'  {
              properties {
                  Item2 = 7.21
              }
          }
          robot 'robot3'  {
              properties inherits from 'robot','robot2'  {
                  Item1 = 'atribut'
              }
          }
      }
       """
    products = extract_model_string(robot_model)

    assert len(products.robots[2].properties) == 2

    assert products.robots[2].properties[1].name == 'Item2' and products.robots[2].properties[1].value == 7.21
    assert products.robots[2].properties[0].name == 'Item1' and products.robots[2].properties[0].value == 'atribut'


def test_inheritance_depth_one_level():
    robot_model = """
      products {
          robot 'robot'   {
              properties   {
                  Item1 = 6.2
              }
          }
          robot 'robot2'   {
              properties inherits from 'robot3'  {
                  Item2 = true
              }
          }
          robot 'robot3'  {
              properties  inherits from 'robot' {
                  Item3 = 'atribut'
              }
          }
      }
    """
    products = extract_model_string(robot_model)
    assert len(products.robots[1].properties) == 3
    assert len(products.robots[2].properties) == 2


def test_inheritance_depth():
    robot_model = """
      products {
          robot 'robot'   {
              properties   {
                  Item1 = 6.2
              }
          }
          robot 'robot2'   {
              properties inherits from 'robot3','robot5'  {
                  Item2 = true
              }
          }
          robot 'robot3'  {
              properties  inherits from 'robot','robot4' {
                  Item3 = 'atribut'
              }
          }
         robot 'robot4'  {
              properties {
                  Item4 = 'atribut2'
              }
         }
         robot 'robot5'  {
              properties  inherits from 'robot' {
                  Item5 = 'atribut3'
              }
         }
      }
    """
    products = extract_model_string(robot_model)
    assert len(products.robots[1].properties) == 5
    assert len(products.robots[2].properties) == 3
    assert len(products.robots[4].properties) == 2


def test_inheritance_depth2():
    robot_model = """
      products {
          robot 'robot'   {
              properties   {
                  Item1 = 6.2
              }
          }
          robot 'robot2'   {
              properties inherits from 'robot3' {
                  Item2 = true
              }
          }
          robot 'robot3'  {
              properties  inherits from 'robot','robot4','robot5' {
                  Item3 = 'atribut'
              }
          }
         robot 'robot4'  {
              properties {
                  Item4 = 'atribut2'
              }
         }
         robot 'robot5'  {
              properties  {
                  Item5 = 'atribut3'
              }
         }
      }
    """
    products = extract_model_string(robot_model)

    assert len(products.robots[1].properties) == 5
    assert len(products.robots[2].properties) == 4


def test_inheritance_depth2_repeating_prop():
    robot_model = """
      products {
          robot 'robot'   {
              properties   {
                  Item1 = 6.2
              }
          }
          robot 'robot2'   {
              properties inherits from 'robot3' {
                  Item2 = true
              }
          }
          robot 'robot3'  {
              properties  inherits from 'robot','robot4','robot5' {
                  Item5 = 'atribut'
              }
          }
         robot 'robot4'  {
              properties {
                  Item4 = 'atribut2'
              }
         }
         robot 'robot5'  {
              properties  {
                  Item5 = 'atribut3'
              }
         }
      }
    """
    products = extract_model_string(robot_model)

    assert len(products.robots[1].properties) == 4
    assert len(products.robots[2].properties) == 3
