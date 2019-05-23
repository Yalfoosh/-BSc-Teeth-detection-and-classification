import os

from typing import Type, Tuple

from util import endswith_in
from values import Image


# region Type Validity
def assert_valid_type(polled_object, supposed_type: Type):
    assert isinstance(polled_object, supposed_type)
# endregion


# region Value Validity
def assert_float_in_range(number: float, interval: Tuple[float, float]):
    assert interval[0] <= number <= interval[1]
# endregion


# region Path Validity
def assert_path_exists(path: str):
    assert os.path.exists(path)


def assert_valid_image(image_path: str):
    assert endswith_in(string=image_path, suffices=Image.image_extensions)
    assert_path_exists(path=image_path)


def assert_valid_xml(xml_file_path: str):
    assert xml_file_path.endswith(".xml")
    assert_path_exists(path=xml_file_path)
# endregion














