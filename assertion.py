import os

from typing import Type, Tuple

from util import endswith_in
from values import Image


# region Type Validity
def assert_valid_type(polled_object, supposed_type: Type):
    assert isinstance(polled_object, supposed_type)
# endregion


# region Value Validity
def assert_int_in_range(number: int, interval: Tuple[int, int]):
    assert interval[0] <= number <= interval[1]


def assert_float_in_range(number: float, interval: Tuple[float, float]):
    assert interval[0] <= number <= interval[1]
# endregion


# region Path Validity
def assert_path_exists(path: str):
    assert os.path.exists(path)


def assert_valid_csv_path(csv_path: str):
    assert csv_path.endswith(".csv")


def assert_valid_image_path(image_path: str):
    assert endswith_in(string=image_path, suffices=Image.image_extensions)


def assert_valid_xml_path(xml_file_path: str):
    assert xml_file_path.endswith(".xml")


def assert_valid_extension(extension: str):
    assert extension.startswith(".") and not extension.endswith(".")
# endregion














