import copy
import os
import xml.etree.ElementTree as ElementTree

from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter
from typing import Iterable, Tuple


import assertion
import selection


class Context:
    acceptable_markings =\
        {
            "11", "12", "13", "14", "15", "16", "17", "18",
            "21", "22", "23", "24", "25", "26", "27", "28",
            "31", "32", "33", "34", "35", "36", "37", "38",
            "41", "42", "43", "44", "45", "46", "47", "48",
            "IMPLANTAT"
        }

    def __init__(self, name: str, markings: Iterable[Tuple[Tuple[int, int, int, int], str]]):
        assertion.assert_valid_type(name, str)

        self.name = name
        self.markings = markings

    @staticmethod
    def from_xml(xml_file_path: str):
        assertion.assert_valid_xml_path(xml_file_path=xml_file_path)

        file_name = Path(xml_file_path).stem
        markings = list()

        xml_root = ElementTree.parse(xml_file_path).getroot()

        for xml_object in xml_root.findall("object"):
            bounding_box, label = ([0, 0, 1, 1], "")

            for bounding_box in xml_object.findall("bndbox"):
                for x_min in bounding_box.findall("xmin"):
                    bounding_box[0] = int(x_min.text)
                    break

                for y_min in bounding_box.findall("ymin"):
                    bounding_box[1] = int(y_min.text)
                    break

                for x_max in bounding_box.findall("xmax"):
                    bounding_box[2] = int(x_max.text)
                    break

                for y_max in bounding_box.findall("ymax"):
                    bounding_box[3] = int(y_max.text)
                    break

                bounding_box = tuple(bounding_box)

            for name in xml_object.findall("name"):
                label = name.text
                break

            markings.append((bounding_box, label))

        return Context(name=file_name, markings=markings)

    def __str__(self):
        to_return = "{}:\n".format(self.name)

        for marking in self.markings:
            to_return += "\t({}, {}) -> ({}, {}) - {}\n".format(*marking[0], marking[1])

        return to_return.strip()

    def to_csv(self, name_appendage: str = "", image_folder: str = None, extension: str = ".jpg"):
        if image_folder is None:
            image_folder = os.path.abspath(os.path.curdir)

        # region Assertions
        assertion.assert_valid_type(name_appendage, str)

        assertion.assert_valid_type(image_folder, str)
        assertion.assert_path_exists(image_folder)

        assertion.assert_valid_type(extension, str)
        assert extension.startswith(".")
        # endregion

        string = ""
        path = os.path.abspath(os.path.join(image_folder, "{}{}{}".format(self.name, name_appendage, extension)))

        for marking in self.markings:
            if marking[0][0] >= marking[0][2] or marking[0][1] >= marking[0][3]:
                continue

            new_class = marking[1]

            if len(marking[1]) is not 2 and marking[1] != "IMPLANTAT":
                if new_class.endswith("I"):
                    new_class = "IMPLANTAT"
                else:
                    new_class = new_class[:2]

                if new_class not in Context.acceptable_markings:
                    continue

            string += "{},{},{},{},{},{}\n".format(path, *marking[0], new_class)

        return string.strip()

    def export_csv(self, destination_path: str, write_mode: selection.WriteMode = selection.WriteMode.Append,
                   name_appendage: str = "", image_folder: str = None, extension: str = ".jpg"):
        assertion.assert_valid_type(destination_path, str)
        assertion.assert_valid_csv_path(destination_path)
        assertion.assert_valid_type(write_mode, selection.WriteMode)

        csv_string = self.to_csv(name_appendage, image_folder, extension).strip() + "\n"

        if write_mode is selection.WriteMode.Overwrite:
            write_mode = "w+"
        elif write_mode is selection.WriteMode.Append:
            write_mode = "a+"

        with open(destination_path, mode=write_mode) as file:
            file.write(csv_string)


class Picture:
    def __init__(self, image_path: str):
        assertion.assert_valid_type(image_path, str)
        assertion.assert_valid_image_path(image_path)

        self._path = Path(image_path)
        self._name = self.path.stem
        self._extension = self.path.suffix

        self.image = Image.open(fp=image_path)
        self.resolution = self.image.size

    # region Properties
    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value: Path or str):
        if isinstance(value, str):
            value = Path(value)

        assertion.assert_valid_type(value, Path)

        self._path = value
        self._name = self._path.stem
        self._extension = self._path.suffix

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        assertion.assert_valid_type(value, str)

        self._name = value
        self._path = Path(os.path.join(self._path.parents[0], self._name + self._extension))

    @property
    def extension(self):
        return self._extension

    @extension.setter
    def extension(self, value):
        assertion.assert_valid_type(value, str)
        assertion.assert_valid_extension(value)

        self._extension = value
        self._path = Path(os.path.join(self._path.parents[0], self._name + self._extension))
    # endregion

    def save(self, path: str):
        assertion.assert_valid_type(path, str)

        self.image.save(path)

    """def resize(self, percentage: float = 0.5):
        assertion.assert_valid_type(percentage, float)
        assertion.assert_float_in_range(percentage, (0.01, 1.0))

        pass"""

    def blur(self, radius: int = 3, new_folder_path: str = None):
        assertion.assert_valid_type(radius, int)
        assertion.assert_int_in_range(radius, (1, int(10e2)))

        if new_folder_path is not None:
            assertion.assert_valid_type(new_folder_path, str)
            assertion.assert_path_exists(new_folder_path)

        new_picture = Picture(str(self.path))
        new_picture.image = new_picture.image.filter(ImageFilter.GaussianBlur(radius=radius))

        if new_folder_path is not None:
            new_picture.path = os.path.join(os.path.abspath(new_folder_path), self.name + self.extension)

        new_picture.name += " blur " + str(radius)

        return new_picture

    def brighten(self, percentage: int or float = 0.0, new_folder_path: str = None):
        if isinstance(percentage, int):
            percentage = float(percentage)

        assertion.assert_valid_type(percentage, float)
        assertion.assert_float_in_range(percentage, (-100.0, int(10e5)))

        if new_folder_path is not None:
            assertion.assert_valid_type(new_folder_path, str)
            assertion.assert_path_exists(new_folder_path)

        brightness_float = 1.0 + percentage / 100.0

        new_picture = Picture(str(self.path))
        new_picture.image = ImageEnhance.Brightness(new_picture.image).enhance(brightness_float)

        if new_folder_path is not None:
            new_picture.path = os.path.join(os.path.abspath(new_folder_path), self.name + self.extension)

        new_picture.name += " "

        if percentage > 0.0:
            new_picture.name += "+"

        new_picture.name += str(round(percentage, 2)) + "%"

        return new_picture


class LabeledImage:
    def __init__(self, picture: Picture, context: Context):
        assertion.assert_valid_type(picture, Picture)
        assertion.assert_valid_type(context, Context)

        self.picture = picture
        self.context = context

    def picture_file_name(self):
        return self.picture.name + self.picture.extension

    def context_file_name(self):
        return self.context.name + ".xml"

    def export(self, csv_path: str):
        assertion.assert_valid_type(csv_path, str)
        assertion.assert_valid_csv_path(csv_path)

        self.picture.save(str(self.picture.path))
        self.context.export_csv(destination_path=csv_path,
                                image_folder=str(self.picture.path.parents[0]), extension=self.picture.extension)

    @staticmethod
    def from_xml(xml_file_path, image_path_prefix: str, extension: str = ".jpg"):
        assertion.assert_valid_type(image_path_prefix, str)
        assertion.assert_path_exists(image_path_prefix)

        assertion.assert_valid_type(extension, str)

        context = Context.from_xml(xml_file_path)

        image_path = os.path.join(image_path_prefix, context.name + extension)

        picture = Picture(image_path)

        return LabeledImage(picture, context)


labeled_images = list()

